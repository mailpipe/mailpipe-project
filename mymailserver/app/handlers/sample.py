import logging
from lamson.routing import route, route_like, stateless
from config.settings import relay
from lamson import view
import requests

try:
    import simplejson as json
except ImportError:
    import json


@route("(address)@(host)", address=".+")
@stateless
def POST(message, address=None, host=None):
    payload = locals()
    url = 'http://code.readevalprint.com:4000/'
    r = requests.post(url, data=payload)

