# MailPipe - Make emails do stuff
[![Build Status](https://travis-ci.org/readevalprint/mailpipe-project.png?branch=master)](https://travis-ci.org/readevalprint/mailpipe-project)

## Goal
Get notifications pushed to a callback url when an email matching an account is received. Provide an API to manage email accounts, callbacks, and emails.

# Usage

### Get your token
```
$ curl -d "username=tim&password=secret" example.com:8000/get_token/
{
    "token": "866ee9de3d36afc0d9d37dle0c901b53r4811623"
}
```
### List accounts (none at first)
```
$ curl -X GET http://example:8000/accounts/ -H 'Authorization: Token 866ee9de3d36afc0d9d37dle0c901b53r4811623'
[]
```

### Make a new email account
The host of the address can include any (sub)domain that is using this mailserver as the MX record.
```
$ curl -X POST -d "address=test@example.com&callback_url=http://my-other-site.com/callback" \
example.com:8000/accounts -H 'Authorization: Token 866ee9de3d36afc0d9d37dle0c901b53r4811623'
{
    "url": "http://example:8000/address/test@example.com/", 
    "address": "test@example.com", 
    "callback_url": "https://my-other-site.com/callback"
}
```
### List your accounts
```
$ curl -X GET http://example:8000/accounts/ -H 'Authorization: Token 866ee9de3d36afc0d9d37dle0c901b53r4811623'
[
    {
        "url": "http://example:8000/accounts/test@example.com/",
        "address": "test@example.com",
        "callback_url": "https://my-other-site.com/callback"
    }
]
```
### List emails recived on your new account (none yet)
```
$ curl -X GET http://example:8000/accounts/test@example.com/ -H 'Authorization: Token 866ee9de3d36afc0d9d37dle0c901b53r4811623'
{
    "url": "http://example.com:8000/accounts/test@example.com/",
    "address": "test@example.com",
    "callback_url": "http://my-other-site.com/callback/", 
    "emails": []
}
```
### Send an email
Email test@example.com
```
$ curl -X GET http://example:8000/accounts -H 'Authorization: Token 866ee9de3d36afc0d9d37dle0c901b53r4811623'
{
    "url": "http://example:8000/accounts/test@example.com/", 
    "address": "test@example.com",
    "callback_url": "http://my-other-site.com/callback", 
    "emails": [
        "http://example.com:8000/emails/1/"
        ]
}
```
### Callback
Now `https://my-other-site.com/callback?email_url=http://example.com:8000/emails/1/` will have been called which you can can now use to retrieve the email message.

```
$ curl -X GET http://example:8000/emails/1/ -H 'Authorization: Token 866ee9de3d36afc0d9d37dle0c901b53r4811623'
{
    "url": "http://example:8000/emails/1/", 
    "id": 1, 
    "text": "bar\n", 
    "html": "<div dir=\"ltr\">bar</div>\n", 
    "to": "\"test+something\" <test+something@example.com>", 
    "frm": "Tim Watts <tim@readevalprint.com>", 
    "subject": "foo", 
    "date": "Tue, 30 Apr 2013 19:33:02 -0700", 
    "attachments": [], 
    "route_url": "http://example:8000/accounts/test", 
    "route": "test", 
    "address": "test+something", 
    "host": "example.com", 
    "created_at": "2013-05-01T02:33:23.385Z"
}
```
### Delete the email
Now that you have read and done stuff to your email, you want to delete it.
```
$ curl -X DELETE http://example:8000/email/1/ -H 'Authorization: Token 866ee9de3d36afc0d9d37dle0c901b53r4811623'
```


# Installation

```
$ mkvirtualenv mailpipe
$ git clone git://github.com/readevalprint/mailpipe-project.git
cd ./mailpipe-project
pip install -r requirements.txt
```

# Setup

### Start lamson on port 25
First find your normal user id and group id. See http://lamsonproject.org/
```
>>> import os
>>> os.getuid()
1001
>>> os.getgid()
1001
>>> ^D
```

Start it as root, and give the uid and gid to drop to.
```
cd ./maileserver
$ sudo `which lamson` start -uid 1001 -gid 1001 
```
### Verify it is running

```
$ telnet YOUR_HOST 25
Trying IP_ADDRESS...
Connected to YOUR_HOST.
Escape character is '^]'.
220 YOUR_HOST Python SMTP proxy version 0.2
```
Press ctr+]
```
^]
telnet> close
Connection closed.
```

### Add your local_settings.py for django 
Specifically you need to set your SECRET_KEY. 

See https://docs.djangoproject.com/en/dev/ref/settings/#secret-key

Here we are using Django to store message. This is not recoomended for production.

See: http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#celerytut-broker
```
# mailpipe/local_settings.py 
from settings import *

INSTALLED_APPS += ('kombu.transport.django', )


SECRET_KEY = 'CHANGE_ME'
BROKER_URL = 'django://'
```

### Create your database
By default we are using sqlite3 but you should alse change that when you deploy. Go ahead and create your admin here too.
```
$ ./manage.py syncdb
```

### Set your Django Site
Here you will want to use the host and port your server is using that is public on the internet.
```
$ ./manage.py shell_plus
In [1]: s = Site.objects.get_current()

In [2]: s.domain = 'http://exmaple.com:8000'

In [3]: s.name = 'example.com'

In [4]: s.save()

In [5]: exit
```

### Start the message queue
Leave this running.
```
./manage.py celeryd -l info
```

### Start the dev server
Do this on a different session (byobu or screen is helpful) and don't forget to use your virtualenv
```
$ workon mailpipe
$ cd mailpipe-project/mailpipe/
$ ./manage.py runserver 0.0.0.0:8000
```
Open your browser and goto http://YOUR_HOST:8000 and sign in as your admin account you made above and follow the instructions.

# Production
I would recommend PostgreSQL, RabbitMQ, Nginx, uwsgi, and of course, serve everything over https

# Authors
@readevalprint

# License
The MIT License (MIT)

Copyright (c) 2013 Timothy John Watts (readevalprint)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

