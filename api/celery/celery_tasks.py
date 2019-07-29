from api import celery

from api.emails.mail_helper import send_email_reminder


@celery.task()
def send_reminder():
    send_email_reminder()
