import email
import string
import random
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_slug
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


class Route(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(validators=[validate_slug],
                            unique=True,
                            max_length=10)
    callback_url = models.URLField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Email(models.Model):
    route = models.ForeignKey(Route, editable=False)
    address = models.CharField(editable=False, max_length=254)
    host = models.CharField(editable=False, max_length=253)
    message = models.TextField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def payload(self):
        #  Cache on the instance
        if hasattr(self, 'd'):
            return self.d
        msg = self.parsed_message()
        d = {}
        attachments = []
        for pl in msg.walk():
            if pl.get_filename():
                attachments += [{'filename': pl.get_filename(),
                    'cid': pl.get('Content-Id', ''),
                    'content_type': pl.get_content_type(),
                    'payload': pl.get_payload()}]
            elif pl.get_content_type() in ['text/html', 'text/plain']:
                d[pl.get_content_type()] = pl.get_payload()
        d['attachments'] = attachments
        d['to'] = msg['To']
        d['subject'] = msg['subject']
        d['from'] = msg['From']
        d['date'] = msg['date']
        self.d = d
        return d

    def frm(self):
        return self.payload().get('from', '')

    def date(self):
        return self.payload().get('date', '')

    def subject(self):
        return self.payload().get('subject', '')

    def to(self):
        return self.payload().get('to', '')

    def html(self):
        return self.payload().get('text/html', '')

    def text(self):
        return self.payload().get('text/plain', '')

    def attachments(self):
        return self.payload()['attachments']

    def parsed_message(self):
        return email.message_from_string(self.message.encode('utf-8'))

    @classmethod
    def create(cls, address, host, message):
        name = address.split('+', 1)[0]
        route = Route.objects.filter(name=name)
        if not route:
            return None
        route = route[0]  # This is ok because Routes are unique on name
        email = cls.objects.create(route=route,
                                   address=address,
                                   host=host,
                                   message=message)
        return email


def attachment_path(instance, filename):
    return '/'.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(3)) + '/'


class Attachment(models.Model):
    email = models.ForeignKey(Email)
    attachment = models.FileField(upload_to=attachment_path)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
