import sys
import os
from lamson.routing import route, stateless


here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)

sys.path.append(here('../../../mailpipe'))
from mailpipe import tasks


@route("(address)@(host)", address=".+")
@stateless
def QUEUE(message, address=None, host=None):
    tasks.process_email.delay(message=message, local=address, host=host)
