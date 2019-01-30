import celery
import requests


@celery.task(name='mailpipe.tasks.process_email')
def process_email(message, local, host):
    from .models import Email
    email = Email.create(message=message, local=local, host=host)
    if email:
        notify_callback.delay(email.id)
    return email


@celery.task(name='mailpipe.tasks.notify_callback')
def notify_callback(email_id, retry_seconds=None, default_retry_delay=60):
    try:
        from django.contrib.sites.models import Site
        from django.core.urls import reverse
        from django.conf import settings
        retry_seconds = retry_seconds or getattr(
            settings, 'MAILPIPE_CALLBACK_RETRY_SECONDS', 60)
        from .models import Email
        email = Email.objects.filter(id=email_id)
        if not email:
            return False
        email = email[0]
        if not email.account.callback_url:
            return False
        retry = True
        try:
            domain = Site.objects.get_current().domain
            path = reverse('email-detail', kwargs={'pk': email.pk})
            r = requests.get(email.account.callback_url,
                             params={'email_url': domain + path})
            if r.status_code == 200:
                retry = False
        except Exception as e:
            print(e)
        if retry and retry_seconds < getattr(settings, 'MAILPIPE_CALLBACK_TIMEOUT_SECONDS', 60 * 60):
            notify_callback.apply_async(
                [email_id], {'retry_seconds': retry_seconds}, countdown=retry_seconds)
        return not retry
    except Exception as exc:
        raise notify_callback.retry(exc=exc)
