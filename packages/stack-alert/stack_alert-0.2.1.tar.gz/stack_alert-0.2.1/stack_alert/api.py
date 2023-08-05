#!/usr/bin/env python3

"""\
Be notified when interesting questions are posted to Stack Exchange sites.

Usage:
    stack_alert [-DN]

Options:
    -D --no-download
        Skip the download step and instead query the questions cached from the 
        previous run.

    -N --no-notify
        Skip the notify step.
"""

import re
import json
import time
import requests
import toml
import logging
import appdirs
import jinja2
import gettext

from pathlib import Path
from datetime import datetime, timedelta
from itertools import count, product
from more_itertools import flatten
from tqdm import tqdm
from inform import plural
from math import floor, ceil
from excerpt_html import excerpt_html
from socket import gethostname
from subprocess import run

DIRS = appdirs.AppDirs('stack_alert')
LOGGER = logging.getLogger('stack_alert')

info = LOGGER.info
warning = LOGGER.warning
error = LOGGER.error
critical = LOGGER.critical

# Data structures
# ===============
# questions:
#   List of dictionaries with information about questions posted on Stack 
#   Exchange sites.  Each dictionary represents a single question and has the 
#   following keys:
#
#   Returned by Stack Exchange API:
#       link (str):
#       title (str)
#       body (str):
#       tags (list):
#       creation_date (epoch time):
#
#   Added by `_download_questions()`:
#       site (str):
#       matching_queries (list):
#
#   Added by `_pick_excerpts()`:
#       excerpt (str):
#
# queries:
#   List of dictionaries containing parameters to identify questions that the 
#   user is interested in being notified of.  Each dictionary has the following 
#   keys:
#
#   sites (set):
#       The Stack Exchange sites to search.
#   keywords (set):
#       Regular expressions that will be applied to both the title and the body 
#       of the question.
#   tags (set):
#       Tags that matching questions must have.
#   recipients (set):
#       The email addresses to be notified when the query is matched.
#
# hits:
#   Those questions that match a query.

def notify(*, download=True, notify=True):
    queries = _load_queries()
    cache = _load_cached_questions()
    sites = set(flatten(x['sites'] for x in queries))
    questions = []

    # Download the most recent questions:
    if not download:
        questions = cache
        info(f"skipping download step; using {len(questions)} cached questions")

    else:
        for site in sites:
            dates = _pick_date_range(site, cache)
            questions += _download_questions(site, dates)

        _prune_stale_questions(questions, cache)
        _update_cached_questions(questions)
        info(f"downloaded {plural(questions):# new question/s} overall")

    # Find any questions that match a query:
    for query, question in product(queries, questions):
        if _eval_query(query, question):
            question['matching_queries'].append(query)

    # Alert the user of any matches:
    hits = [x for x in questions if x['matching_queries']]
    info(f"found {plural(hits):# question/s} matching queries")

    if notify:
        _notify_recipients(queries, hits)
    else:
        info("skipping notification step")


def _load_queries(dirs=DIRS):
    config_path = _get_config_path(dirs)
    if not config_path.exists():
        raise ConfigError(f"{config_path}: file not found")

    def make_query(raw_query):
        query = raw_query.copy()
        make_key(query, 'site', 'sites')
        make_key(query, 'tag', 'tags')
        make_key(query, 'keyword', 'keywords')
        make_key(query, 'recipient', 'recipients')
        return query

    def make_key(query, key_1, key_n):
        if key_1 in query and key_n in query:
            raise ConfigError(f"{config_path}: cannot specify both {key_1!r} and {key_n!r}")

        elif key_n in query:
            query[key_n] = set(query[key_n])
        elif key_1 in query:
            query[key_n] = {query.pop(key_1)}
        else:
            query[key_n] = set()

    def apply_defaults(query, defaults):
        for key in defaults:
            if not query[key]:
                query[key] = defaults[key]

    def check_query(query):
        if not query.get('sites'):
            raise ConfigError(f"{config_path}: no site specified")
        if not query.get('recipients'):
            raise ConfigError(f"{config_path}: no recipient specified")
        if not any(query.get(x) for x in ['tags', 'keywords']):
            raise ConfigError(f"{config_path}: no search parameters specified")

    raw_config = toml.load(config_path)
    defaults = make_query(raw_config.get('default', {}))
    queries = []

    if 'query' not in raw_config:
        raise ConfigError(f"{config_path}: no [[query]] sections specified")

    for raw_query in raw_config['query']:
        query = make_query(raw_query)
        apply_defaults(query, defaults)
        check_query(query)
        queries.append(query)

    info(f"found {plural(queries):# /query/queries} in {config_path}")
    return queries

def _load_cached_questions(dirs=DIRS):
    cache_path = _get_cache_path(dirs)
    if not cache_path.exists():
        return []

    try:
        with cache_path.open() as f:
            return json.load(f)

    except json.JSONDecodeError:
        warning("ignoring cache due to corruption")
        return []

def _update_cached_questions(questions, dirs=DIRS):
    if not questions:
        return

    cache_path = _get_cache_path(dirs)
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    with cache_path.open('w') as f:
        json.dump(questions, f)

def _download_questions(site, dates):
    """
    Repeatedly query the Stack Exchange API to download all questions posted to 
    the given site in the given date range.

    Rate limits requested by the Stack Exchange server are respected.
    """

    # Note that there's a python library that provides access to the Stack 
    # Exchange API (called StackAPI), but it doesn't appear to have the ability 
    # to continue querying the API until all questions have been downloaded.  
    # So instead we implement the calls ourselves.

    url = 'https://api.stackexchange.com/2.2/questions'
    params = dict(
            site=site,
            sort='creation',
            order='desc',
            filter='withbody',
            fromdate=int(floor(dates[0])),  # Timestamps in python are floats,
            todate=int(ceil(dates[1])),     # but Stack Exchange requires ints.
            pagesize=100,
    )
    questions = []

    for page_num in tqdm(count(1)):
        # Make the request, and keep track of how long it takes.
        t0 = time.perf_counter()
        r = requests.get(url, params={**params, 'page': page_num})
        t1 = time.perf_counter()

        # Parse the response.
        wrapper = r.json()

        if 'items' in wrapper:
            questions += wrapper.pop('items')

        if not wrapper.get('has_more'):
            break

        if not wrapper['quota_remaining']:
            warning(f"reached daily quota of {wrapper['quota_max']} Stack Exchange API requests; some questions may not have been downloaded")
            break

        # Sleep for long enough to not get throttled.  There is a 30 request/sec 
        # hard-limit, but in practice this is hard to reach because each request 
        # seems to take about 0.15 sec.  The API may also request that we sleep for 
        # some time by sending us the "backoff" parameter, so respect that.
        dt = max(1/15 - (t1-t0), wrapper.get('backoff', 0))
        time.sleep(dt)

    for q in questions:
        q['site'] = site
        q['matching_queries'] = []

    info(f"downloaded {plural(questions):# question/s} posted to {site!r} between {datetime.fromtimestamp(dates[0])} and {datetime.fromtimestamp(dates[1])}")
    return questions

def _pick_date_range(site, cache):
    curr_date = datetime.now().timestamp()
    site_cache = [x for x in cache if x['site'] == site]

    if site_cache:
        last_date = max(x['creation_date'] for x in site_cache)
    else:
        yesterday = datetime.now() - timedelta(days=1)
        last_date = yesterday.timestamp()

    return last_date, curr_date

def _prune_stale_questions(questions, cache):
    stale_ids = set(x['question_id'] for x in cache)
    return [x for x in questions if x['question_id'] not in stale_ids]

def _eval_query(query, question):
    return all([
            _eval_site(query, question),
            _eval_tags(query, question),
            _eval_keywords(query, question),
    ])

def _eval_site(query, question):
    return question['site'] in query['sites']
            
def _eval_tags(query, question):
    return all(x in question['tags'] for x in query['tags'])

def _eval_keywords(query, question):
    patterns = query['keywords']
    strings = question['title'], question['body']

    if not patterns:
        return True

    for pattern, string in product(patterns, strings):
        if re.search(pattern, string, re.IGNORECASE):
            return True

    return False

def _get_config_path(dirs=DIRS):
    return Path(dirs.user_config_dir) / 'config.toml'

def _get_cache_path(dirs=DIRS):
    return Path(dirs.user_cache_dir) / 'questions.json'

def _notify_recipients(queries, questions):
    recipients = set(flatten(x['recipients'] for x in queries))
    _pick_excerpts(questions)

    for recipient in recipients:
        qs = _filter_questions_by_recipient(questions, recipient)
        _send_email(recipient, qs)

def _pick_excerpts(questions):
    for question in questions:
        question['excerpt'] = _pick_excerpt(question)

def _pick_excerpt(question):
    # This just takes the first few sentences of the question body.  A smarter 
    # approach would center the excerpt around any matched keywords (and 
    # highlight the keywords).
    #
    # I have also noticed cases where <code> blocks get included and end up 
    # distorting the spacing in the email.  This might also be something to 
    # avoid.
    body = question['body']
    return excerpt_html(body, min_words=35, cut_mark=None) or body

def _send_email(recipient, questions):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.utils import formatdate

    env = jinja2.Environment(
        loader=jinja2.PackageLoader('stack_alert'),
        autoescape=False,
        extensions=[
            'jinja2.ext.i18n',
        ],
    )
    template = env.get_template('email_template.html.jinja')
    html = template.render(
            recipient=recipient,
            questions=questions,
            host=gethostname(),
            datetime=datetime,
            gettext=gettext.gettext,
            ngettext=gettext.ngettext,
    )

    message = MIMEMultipart('alternative')
    if questions:
        message['Subject'] = "New questions posted on Stack Exchange"
    else:
        message['Subject'] = "No new questions posted on Stack Exchange"
    message['To'] = recipient
    message['Date'] = formatdate(localtime=True)
    message.attach(MIMEText(html, 'html'))

    sendmail = 'sendmail', '-t'
    run(sendmail, input=message.as_string(), text=True)
    info(f"sent email to {recipient}")

def _filter_questions_by_recipient(questions, recipient):
    return [
            question
            for question in questions
            if any(
                recipient in query['recipients']
                for query in question['matching_queries']
            )
    ]


class ConfigError(Exception):
    pass
