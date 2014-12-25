import logging
import sys
import os
from salmon.routing import route, stateless

here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)

sys.path.append(here('../../../mailpipe'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'mailpipe.local_settings'

from mailpipe import settings
from mailpipe import tasks
from celery import Celery

# Bit of a work around to get celery to send django tasks to worker.
celery = Celery()
celery.conf.BROKER_URL = settings.BROKER_URL


@route("(address)@(host)", address=".+", host='.+')
@stateless
def QUEUE(message, address=None, host=None):
    result = celery.send_task(tasks.process_email.name, kwargs={'message':message, 'local':address, 'host':host})

