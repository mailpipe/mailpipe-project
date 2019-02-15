import logging
import sys
import os
from salmon.routing import route, stateless

here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)
import logging


sys.path.append(here('../../../mailpipe'))
#os.environ['DJANGO_SETTINGS_MODULE'] = 'mailpipe.settings'

import django
django.setup()

#from django.conf import settings
from mailpipe import tasks
#from celery import Celery



# Bit of a work around to get celery to send django tasks to worker.
#app = Celery('mailpipe')
#app.config_from_object('django.conf:settings', namespace='CELERY')



@route("(address)@(host)", address=".+", host='.+')
@stateless
def QUEUE(message, address=None, host=None):
    result = tasks.process_email(**{'message':message.Data.decode(), 'local':address, 'host':host})

