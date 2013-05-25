import email
import string
import random
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_slug, RegexValidator
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.contrib.sites.models import get_current_site
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


class EmailAccount(models.Model):
    owner = models.ForeignKey(User, related_name="accounts")
    address = models.EmailField(unique=True, validators=[RegexValidator(regex='^[^+]+$', message="Cannot contain labels")])
    callback_url = models.URLField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Email(models.Model):
    account = models.ForeignKey(EmailAccount, editable=False, related_name='emails')
    message = models.TextField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def payload(self):
        #  Cache on the instance
        if hasattr(self, 'd'):
            return self.d
        msg = self.parsed_message()
        d = {}
        attachments = {}
        for pl in msg.walk():
            if pl.get_filename():
                content_id = pl.get('X-Attachment-Id', '')
                filename = pl.get_filename()
                attachments[content_id]= {
                    'filename': filename,
                    'content_type': pl.get_content_type(),
                    'attachment_url': (get_current_site(None).domain +
                                    reverse('email-attachment',
                                            kwargs={'email_pk': self.pk,
                                                    'name': filename,
                                                    'content_id': content_id})),
                    }
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

    def raw_attachments(self):
        msg = self.parsed_message()
        d = {}
        attachments = {}
        for pl in msg.walk():
            if pl.get_filename():
                content_id = pl.get('X-Attachment-Id', '')
                filename = pl.get_filename()
                attachments[content_id] = {
                    'filename': filename,
                    'content_type': pl.get_content_type(),
                    'payload': pl.get_payload()}
        return attachments


    def attachments(self):
        return self.payload()['attachments']

    def parsed_message(self):
        return email.message_from_string(self.message.encode('utf-8'))

    @classmethod
    def create(cls, local, host, message):
        address = local.split('+', 1)[0] + '@' + host
        account = EmailAccount.objects.filter(address=address)
        if not account:
            return None
        account = account[0]
        email = cls.objects.create(account=account,
                                   message=message)
        return email


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
