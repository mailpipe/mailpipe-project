import celery
import requests


@celery.task(name='mailpipe.tasks.process_email')
def process_email(message, local, host):
    from models import Email
    email = Email.create(message=message, local=local, host=host)
    if email:
        notify_callback.delay(email.id)
    return email


@celery.task(name='mailpipe.tasks.notify_callback')
def notify_callback(email_id, timeout=1):
    from models import Email
    email = Email.objects.filter(id=email_id)
    if not email:
        return False
    email = email[0]
    retry = True
    try:
        r = requests.get(email.account.callback_url)
        if r.status_code == 200:
            retry = False
    except:
        pass
    if retry and timeout < 60 * 60: # TODO: Make setting
        notify_callback.apply_async([email_id], {'timeout': timeout*2}, countdown=timeout)
    return not retry
