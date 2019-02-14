# This file contains python variables that configure Salmon for email processing.

# You may add additional parameters such as `username' and `password' if your
# relay server requires authentication, `starttls' (boolean) or `ssl' (boolean)
# for secure connections.
relay_config = {}

receiver_config = {'host': '0.0.0.0', 'port': 25}

handlers = ['app.handlers.sample']

router_defaults = {'host': '.+'}

# the config/boot.py will turn these values into variables set in settings
