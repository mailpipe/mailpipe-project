relay_config = {'host': 'localhost', 'port': 8825}
receiver_config = {'host': '0.0.0.0', 'port': 25}
handlers = ['app.handlers.process']
template_config = {'dir': 'app', 'module': 'templates'}
router_defaults = {}
try:
    from local_settings import *
except Exception as e:
    print "Coulding load local_settings:", e
