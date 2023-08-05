#!/usr/bin/env python3

import pytest, os
import stack_alert.api

from stack_alert import *
from textwrap import dedent
from datetime import datetime

@pytest.fixture
def tmp_appdir(tmp_path):

    class AppDirs:
        pass

    app_dirs = AppDirs()
    app_dirs.user_config_dir = tmp_path / 'config'
    app_dirs.user_cache_dir = tmp_path / 'cache'

    print(tmp_path)
    yield app_dirs


@pytest.mark.parametrize(
        'params', [
            dict(
                toml="""\
                    [[query]]
                    site = 'stackoverflow'
                    tag = 'python'
                    recipient = 'alice@example.com'
                """,
                expected=[
                    dict(
                        sites={'stackoverflow'},
                        tags={'python'},
                        keywords=set(),
                        recipients={'alice@example.com'},
                    ),
                ],
            ),

            dict(
                toml="""\
                    [[query]]
                    site = 'stackoverflow'
                    tag = 'python'
                    recipient = 'alice@example.com'

                    [[query]]
                    site = 'stackoverflow'
                    keyword = '(num|sci)py'
                    recipient = 'bob@example.com'
                """,
                expected=[
                    dict(
                        sites={'stackoverflow'},
                        tags={'python'},
                        keywords=set(),
                        recipients={'alice@example.com'},
                    ),
                    dict(
                        sites={'stackoverflow'},
                        tags=set(),
                        keywords={'(num|sci)py'},
                        recipients={'bob@example.com'},
                    ),
                ],
            ),

            dict(
                toml="""\
                    [[query]]
                    sites = ['stackoverflow']
                    tags = ['python', 'math']
                    recipients = ['alice@example.com']
                """,
                expected=[
                    dict(
                        sites={'stackoverflow'},
                        tags={'python', 'math'},
                        keywords=set(),
                        recipients={'alice@example.com'},
                    ),
                ],
            ),

            dict(
                toml="""\
                    [[query]]
                    site = 'stackoverflow'
                    keyword = '(num|sci)py'
                    recipient = 'alice@example.com'
                """,
                expected=[
                    dict(
                        sites={'stackoverflow'},
                        tags=set(),
                        keywords={'(num|sci)py'},
                        recipients={'alice@example.com'},
                    ),
                ],
            ),

            dict(
                toml="""\
                    [[query]]
                    site = 'stackoverflow'
                    keywords = ['(num|sci)py']
                    recipient = 'alice@example.com'
                """,
                expected=[
                    dict(
                        sites={'stackoverflow'},
                        tags=set(),
                        keywords={'(num|sci)py'},
                        recipients={'alice@example.com'},
                    ),
                ],
            ),

            dict(
                toml="""\
                    [default]
                    site = 'stackoverflow'
                    tag = 'python'
                    keyword = '(num|sci)py'
                    recipient = 'alice@example.com'

                    [[query]]
                """,
                expected=[
                    dict(
                        sites={'stackoverflow'},
                        tags={'python'},
                        keywords={'(num|sci)py'},
                        recipients={'alice@example.com'},
                    ),
                ],
            ),

            dict(
                toml="""\
                    [default]
                    site = 'stackoverflow'
                    recipient = 'alice@example.com'
                    keyword = 'a'

                    [[query]]
                    keyword = 'b'
                """,
                expected=[
                    dict(
                        sites={'stackoverflow'},
                        recipients={'alice@example.com'},
                        tags=set(),
                        keywords={'b'},
                    ),
                ],
            ),

            dict(
                toml="""\
                    [default]
                    site = 'stackoverflow'
                    recipient = 'alice@example.com'
                    keywords = ['a', 'b']

                    [[query]]

                    [[query]]
                    keyword = 'c'
                """,
                expected=[
                    dict(
                        sites={'stackoverflow'},
                        recipients={'alice@example.com'},
                        tags=set(),
                        keywords={'a', 'b'},
                    ),
                    dict(
                        sites={'stackoverflow'},
                        recipients={'alice@example.com'},
                        tags=set(),
                        keywords={'c'},
                    ),
                ],
            ),

            dict(
                toml="""\
                    [default]
                    site = 'stackoverflow'
                    recipient = 'alice@example.com'
                    keyword = 'a'

                    [[query]]

                    [[query]]
                    keywords = ['b', 'c']
                """,
                expected=[
                    dict(
                        sites={'stackoverflow'},
                        recipients={'alice@example.com'},
                        tags=set(),
                        keywords={'a'},
                    ),
                    dict(
                        sites={'stackoverflow'},
                        recipients={'alice@example.com'},
                        tags=set(),
                        keywords={'b', 'c'},
                    ),
                ],
            ),

            dict(
                toml="""\
                    [default]
                    site = 'stackoverflow'
                    recipient = 'alice@example.com'
                    keywords = ['a', 'b']

                    [[query]]

                    [[query]]
                    keywords = ['c', 'd']
                """,
                expected=[
                    dict(
                        sites={'stackoverflow'},
                        recipients={'alice@example.com'},
                        tags=set(),
                        keywords={'a', 'b'},
                    ),
                    dict(
                        sites={'stackoverflow'},
                        recipients={'alice@example.com'},
                        tags=set(),
                        keywords={'c', 'd'},
                    ),
                ],
            ),

        ]
)
def test_load_queries(tmp_appdir, params):
    _write_config(tmp_appdir, params['toml'])
    assert stack_alert.api._load_queries(tmp_appdir) == params['expected']

@pytest.mark.parametrize(
        'params', [
            dict(
                toml="""\
                """,
                err=r"no \[\[query\]\] sections specified",
            ),

            dict(
                toml="""\
                    [[query]]
                    recipient = "alice@example.com"
                """,
                err="no site specified",
            ),

            dict(
                toml="""\
                    [[query]]
                    site = "stackoverflow"
                """,
                err="no recipient specified",
            ),
        ]
)
def test_load_queries_err(tmp_appdir, params):
    _write_config(tmp_appdir, params['toml'])
    with pytest.raises(ConfigError, match=params['err']):
        stack_alert.api._load_queries(tmp_appdir)

def test_load_queries_err_not_found(tmp_appdir):
    with pytest.raises(ConfigError, match="file not found"):
        stack_alert.api._load_queries(tmp_appdir)

def test_load_cached_questions_1(tmp_appdir):
    assert stack_alert.api._load_cached_questions(tmp_appdir) == []

def test_load_cached_questions_2(tmp_appdir):
    cache = [
            dict(question_id=1),
    ]
    _write_cache(tmp_appdir, cache)
    assert stack_alert.api._load_cached_questions(tmp_appdir) == cache

def test_update_cached_questions_1(tmp_appdir):
    cache = [
            dict(question_id=1),
    ]
    _write_cache(tmp_appdir, cache)
    stack_alert.api._update_cached_questions([])

    assert stack_alert.api._load_cached_questions(tmp_appdir) == cache

@pytest.mark.parametrize(
        'params', [
            dict(
                old_cache=[dict(question_id=1)],
                new_cache=[dict(question_id=2)],
                expected= [dict(question_id=2)],
            ),
            dict(
                old_cache=[dict(question_id=1)],
                new_cache=[],
                expected= [dict(question_id=1)],
            ),
        ]
)
def test_update_cached_questions_1(tmp_appdir, params):
    _write_cache(tmp_appdir, params['old_cache'])
    stack_alert.api._update_cached_questions(params['new_cache'], tmp_appdir)
    assert stack_alert.api._load_cached_questions(tmp_appdir) == params['expected']

@pytest.mark.parametrize(
        'params', [
            dict(
                now=datetime(2020, 7, 12),
                site='stackoverflow',
                cache=[],
                last_date=datetime(2020, 7, 11),
                curr_date=datetime(2020, 7, 12),
            ),

            dict(
                now=datetime(2020, 7, 12),
                site='stackoverflow',
                cache=[
                    dict(
                        creation_date=datetime(2020, 7, 10).timestamp(),
                        site='stackoverflow',
                    ),
                ],
                last_date=datetime(2020, 7, 10),
                curr_date=datetime(2020, 7, 12),
            ),

            dict(
                now=datetime(2020, 7, 12),
                site='stackoverflow',
                cache=[
                    dict(
                        creation_date=datetime(2020, 7, 9).timestamp(),
                        site='stackoverflow',
                    ),
                    dict(
                        creation_date=datetime(2020, 7, 10).timestamp(),
                        site='stackoverflow',
                    ),
                ],
                last_date=datetime(2020, 7, 10),
                curr_date=datetime(2020, 7, 12),
            ),

            dict(
                now=datetime(2020, 7, 12),
                site='stackoverflow',
                cache=[
                    dict(
                        creation_date=datetime(2020, 7, 10).timestamp(),
                        site='bioinformatics',
                    ),
                ],
                last_date=datetime(2020, 7, 11),
                curr_date=datetime(2020, 7, 12),
            ),

            dict(
                now=datetime(2020, 7, 12),
                site='stackoverflow',
                cache=[
                    dict(
                        creation_date=datetime(2020, 7, 9).timestamp(),
                        site='stackoverflow',
                    ),
                    dict(
                        creation_date=datetime(2020, 7, 10).timestamp(),
                        site='bioinformatics',
                    ),
                ],
                last_date=datetime(2020, 7, 9),
                curr_date=datetime(2020, 7, 12),
            ),
        ]
)
def test_pick_date_range(monkeypatch, params):
    _mock_datetime_now(monkeypatch, params['now'])
    dates = stack_alert.api._pick_date_range(params['site'], params['cache'])
    assert dates == (
            params['last_date'].timestamp(),
            params['curr_date'].timestamp(),
    )

@pytest.mark.parametrize(
        'params', [
            dict(
                questions=[],
                cache=[],
                expected=[],
            ),

            dict(
                questions=[
                    dict(question_id=1),
                ],
                cache=[],
                expected=[
                    dict(question_id=1),
                ],
            ),

            dict(
                questions=[
                    dict(question_id=1),
                ],
                cache=[
                    dict(question_id=1),
                ],
                expected=[],
            ),

            dict(
                questions=[
                    dict(question_id=1),
                    dict(question_id=2),
                ],
                cache=[
                    dict(question_id=1),
                ],
                expected=[
                    dict(question_id=2),
                ],
            ),
        ]
)
def test_prune_stale_questions(params):
    questions = stack_alert.api._prune_stale_questions(
            params['questions'],
            params['cache'],
    )
    assert questions == params['expected']

@pytest.mark.parametrize(
        'params', [

            # Everything matches:
            dict(
                query=dict(
                    sites={'stackoverflow'},
                    tags={'python'},
                    keywords={'(num|sci)py'},
                ),
                question=dict(
                    site='stackoverflow',
                    title="Problem with numpy",
                    body="Here is a problem...",
                    tags=['python', 'numpy'],
                ),
                expected=True,
            ),

            # Empty parameters are ignored:
            dict(
                query=dict(
                    sites={'stackoverflow'},
                    tags={'python'},
                    keywords=set(),
                ),
                question=dict(
                    site='stackoverflow',
                    title="Problem with python",
                    body="Here is a problem...",
                    tags=['python', 'numpy'],
                ),
                expected=True,
            ),

            dict(
                query=dict(
                    sites={'stackoverflow'},
                    tags=set(),
                    keywords={'(num|sci)py'},
                ),
                question=dict(
                    site='stackoverflow',
                    title="Problem with numpy",
                    body="Here is a problem...",
                    tags=['python', 'numpy'],
                ),
                expected=True,
            ),

            # Keywords are regular expressions:
            dict(
                query=dict(
                    sites={'stackoverflow'},
                    tags=set(),
                    keywords={'(num|sci)py'},
                ),
                question=dict(
                    site='stackoverflow',
                    title="Problem with scipy",
                    body="Here is a problem...",
                    tags=['python'],
                ),
                expected=True,
            ),

            # The correct fields are searched for keywords:
            dict(
                query=dict(
                    sites={'stackoverflow'},
                    tags=set(),
                    keywords={'(num|sci)py'},
                ),
                question=dict(
                    site='stackoverflow',
                    title="Problem with something",
                    body="Here is a problem with numpy...",
                    tags=['python', 'numpy'],
                ),
                expected=True,
            ),

            dict(
                query=dict(
                    sites={'stackoverflow'},
                    tags=set(),
                    keywords={'(num|sci)py'},
                ),
                question=dict(
                    site='stackoverflow',
                    title="Problem with something",
                    body="Here is a problem...",
                    tags=['python', 'numpy'],
                ),
                expected=False,
            ),

            # Multiple tags:
            dict(
                query=dict(
                    sites={'stackoverflow'},
                    tags={'python', 'numpy'},
                    keywords=set(),
                ),
                question=dict(
                    site='stackoverflow',
                    title="Problem with python",
                    body="Here is a problem...",
                    tags=['python', 'numpy'],
                ),
                expected=True,
            ),

            dict(
                query=dict(
                    sites={'stackoverflow'},
                    tags={'python', 'numpy'},
                    keywords=set(),
                ),
                question=dict(
                    site='stackoverflow',
                    title="Problem with python",
                    body="Here is a problem...",
                    tags=['python'],
                ),
                expected=False,
            ),


            # Mismatches:
            dict(
                query=dict(
                    sites={'wrong-site'},
                    tags={'python'},
                    keywords={'(num|sci)py'},
                ),
                question=dict(
                    site='stackoverflow',
                    title="Problem with numpy",
                    body="Here is a problem...",
                    tags=['python', 'numpy'],
                ),
                expected=False,
            ),

            dict(
                query=dict(
                    sites={'stackoverflow'},
                    tags={'wrong-tag'},
                    keywords={'(num|sci)py'},
                ),
                question=dict(
                    site='stackoverflow',
                    title="Problem with numpy",
                    body="Here is a problem...",
                    tags=['python', 'numpy'],
                ),
                expected=False,
            ),

            dict(
                query=dict(
                    sites={'stackoverflow'},
                    tags={'python'},
                    keywords={'wrong-keyword'},
                ),
                question=dict(
                    site='stackoverflow',
                    title="Problem with numpy",
                    body="Here is a problem...",
                    tags=['python', 'numpy'],
                ),
                expected=False,
            ),
        ]
)
def test_eval_query(params):
    is_match = stack_alert.api._eval_query(params['query'], params['question'])
    assert is_match == params['expected']

@pytest.mark.parametrize(
        'params', [

            # 0 questions:
            dict(
                questions=[],
                recipient='alice@example.com',
                expected=set(),
            ),

            # 1 question, 1 query, 1 recipient:
            dict(
                questions=[
                    dict(
                        question_id=1,
                        matching_queries=[
                            dict(
                                recipients=['alice@example.com'],
                            ),
                        ],
                    ),
                ],
                recipient='alice@example.com',
                expected={1},
            ),

            dict(
                questions=[
                    dict(
                        question_id=1,
                        matching_queries=[
                            dict(
                                recipients=['alice@example.com'],
                            ),
                        ],
                    ),
                ],
                recipient='bob@example.com',
                expected=set(),
            ),

            # 1 question, 1 query, 2 recipients
            dict(
                questions=[
                    dict(
                        question_id=1,
                        matching_queries=[
                            dict(
                                recipients=[
                                    'alice@example.com',
                                    'bob@example.com',
                                ],
                            ),
                        ],
                    ),
                ],
                recipient='alice@example.com',
                expected={1},
            ),

            dict(
                questions=[
                    dict(
                        question_id=1,
                        matching_queries=[
                            dict(
                                recipients=[
                                    'alice@example.com',
                                    'bob@example.com',
                                ],
                            ),
                        ],
                    ),
                ],
                recipient='bob@example.com',
                expected={1},
            ),

            # 1 question, 2 queries, 1 recipient each
            dict(
                questions=[
                    dict(
                        question_id=1,
                        matching_queries=[
                            dict(
                                recipients=[
                                    'alice@example.com',
                                ],
                            ),
                            dict(
                                recipients=[
                                    'bob@example.com',
                                ],
                            ),
                        ],
                    ),
                ],
                recipient='alice@example.com',
                expected={1},
            ),

            dict(
                questions=[
                    dict(
                        question_id=1,
                        matching_queries=[
                            dict(
                                recipients=[
                                    'alice@example.com',
                                ],
                            ),
                            dict(
                                recipients=[
                                    'bob@example.com',
                                ],
                            ),
                        ],
                    ),
                ],
                recipient='bob@example.com',
                expected={1},
            ),

            # 2 questions, 1 query each, 1 recipient each
            dict(
                questions=[
                    dict(
                        question_id=1,
                        matching_queries=[
                            dict(
                                recipients=[
                                    'alice@example.com',
                                ],
                            ),
                        ],
                    ),
                    dict(
                        question_id=2,
                        matching_queries=[
                            dict(
                                recipients=[
                                    'bob@example.com',
                                ],
                            ),
                        ],
                    ),
                ],
                recipient='alice@example.com',
                expected={1},
            ),

            dict(
                questions=[
                    dict(
                        question_id=1,
                        matching_queries=[
                            dict(
                                recipients=[
                                    'alice@example.com',
                                ],
                            ),
                        ],
                    ),
                    dict(
                        question_id=2,
                        matching_queries=[
                            dict(
                                recipients=[
                                    'bob@example.com',
                                ],
                            ),
                        ],
                    ),
                ],
                recipient='bob@example.com',
                expected={2},
            ),
        ]
)
def test_filter_questions_by_recipient(params):
    qs = stack_alert.api._filter_questions_by_recipient(
            params['questions'],
            params['recipient'],
    )
    assert {q['question_id'] for q in qs} == params['expected']


def _write_config(tmp_appdir, toml):
    config_path = stack_alert.api._get_config_path(tmp_appdir)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(dedent(toml))

def _write_cache(tmp_appdir, cache):
    config_path = stack_alert.api._get_cache_path(tmp_appdir)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open('w') as f:
        json.dump(cache, f)

def _mock_datetime_now(monkeypatch, value):
    import datetime

    class mock_datetime:
        @classmethod
        def now(cls):
            return value

    monkeypatch.setattr('stack_alert.api.datetime', mock_datetime)

