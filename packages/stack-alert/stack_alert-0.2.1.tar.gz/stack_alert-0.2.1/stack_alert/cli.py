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

import docopt
import logging
from . import notify

def main():
    logging.basicConfig(level=logging.INFO)
    args = docopt.docopt(__doc__)
    notify(
            download=not args['--no-download'],
            notify=not args['--no-notify'],
    )
