***********
Stack Alert
***********

Stack Alert is a program to notify you when a question matching certain filters 
is asked on a Stack Exchange site.  Stack Exchange has a feature that allows 
you to be notified when questions matching certain tags are asked, but this is 
often so broad as to be useless.  Stack Alert instead allows you to filter 
using regular expressions against the title and body of the question.

.. image:: https://img.shields.io/pypi/v/stack_alert.svg
   :target: https://pypi.python.org/pypi/stack_alert

.. image:: https://img.shields.io/pypi/pyversions/stack_alert.svg
   :target: https://pypi.python.org/pypi/stack_alert

.. image:: https://img.shields.io/readthedocs/stack_alert.svg
   :target: https://stack_alert.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/github/workflow/status/kalekundert/stack_alert/Test%20and%20release/master
   :target: https://github.com/kalekundert/stack_alert/actions

.. image:: https://img.shields.io/coveralls/kalekundert/stack_alert.svg
   :target: https://coveralls.io/github/kalekundert/stack_alert?branch=master

Getting Started
===============
Install ``stack_alert`` using ``pip``, preferably into a clean virtual environment::

    $ python -m venv ~/stack_alert_venv
    $ ~/stack_alert_venv/bin/activate
    $ pip install stack_alert

Specify which questions you want to receive alerts for::

  $ vi ~/.config/stack_alert/config.toml
  [[query]]
  site = 'stackoverflow'
  tag = 'python'
  keywords = '(num|sci)py'  # regular expression
  recipient = 'alice@example.com'
  
Configure `cron` to call ``stack_alert`` at 5:00 PM every day.  Log messages 
are written to stderr.  I recommend using `ts 
<http://joeyh.name/code/moreutils/>`__ and `tinylog 
<http://b0llix.net/perp/site.cgi?page=tinylog.8>`__ to collect and rotate these 
messages::

  $ which sendmail
  /usr/sbin/sendmail
  $ crontab -e
  PATH=$HOME/stack_alert_venv/bin:/usr/sbin:/usr/bin:/bin
  0 17 * * * stack_alert 2>&1 | ts | tinylog /path/to/log/dir
