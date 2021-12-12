# Create your tasks here
from __future__ import absolute_import, unicode_literals

from django.core.mail import EmailMultiAlternatives
from django_rq import job

from application.settings import GENERAL_QUEUE


@job(GENERAL_QUEUE)
def notify_user_by_email(subject, body, html_body, sender, receiver):
    email_msg = EmailMultiAlternatives(
        subject, body,
        sender, receiver,
    )
    email_msg.attach_alternative(html_body, "text/html")
    email_msg.send()
    return True

