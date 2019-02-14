import logging
import sys
import os
from salmon.routing import route, stateless

here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)


from celery import Celery

# Bit of a work around to get celery to send django tasks to worker.
celery = Celery()
celery.conf.broker_url = os.environ.get("BROKER_URL", "amqp://myuser:mypassword@rabbitmq:5672/myvhost") 
celery.conf.task_serializer = 'pickle'


@route("(address)@(host)", address=".+", host='.+', task_serializer='pickle')
@stateless
def QUEUE(message, address=None, host=None):
    print(message.__dict__)
    #result = celery.send_task("tasks.process_email.name", kwargs={'message':message, 'local':address, 'host':host})
    result = celery.send_task("tasks.process_email.name", kwargs={'message':message, 'local':address, 'host':host})

