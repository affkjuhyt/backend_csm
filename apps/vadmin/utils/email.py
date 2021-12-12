import logging

from django.template.loader import get_template
from rest_registration.utils.users import get_user_setting

from application import email
from userprofile.tasks import notify_user_by_email

logger = logging.getLogger(__name__.split('.')[0])


class EmailUserNotification(object):
    def __init__(self, user, host):
        self.user = user
        self.username = user.userprofile.full_name
        self.login_name = user.username
        self.user_email = user.email
        host = f'https://{host}'
        self.base_context = {
            'logo_png': f'{host}/{email.BITHR_LOGO_PNG}',
            'facebook_url': email.FACEBOOK_URL,
            'facebook_png': f'{host}/{email.FACEBOOK_PNG}',
            'twitter_url': email.TWITTER_URL,
            'twitter_png': f'{host}/{email.TWITTER_PNG}',
            'telegram_url': email.TELEGRAM_URL,
            'telegram_png': f'{host}/{email.TELEGRAM_PNG}',
            'youtube_url': email.YOUTUBE_URL,
            'youtube_png': f'{host}/{email.YOUTUBE_PNG}',
            'google_play_png': f'{host}/{email.GOOGLE_PLAY_PNG}',
            'apple_store_png': f'{host}/{email.APPLE_STORE_PNG}',
        }

    @classmethod
    def send_email(cls, subject, body, html, receiver, sender=email.EMAIL_NOTIFICATION_SENDER, is_background=True):
        try:
            if is_background:
                notify_user_by_email.delay(subject, body, html, sender, receiver)
            else:
                notify_user_by_email(subject=subject,
                                     body=body,
                                     sender=sender,
                                     html_body=html,
                                     receiver=receiver)
        except Exception as e:
            logger.error('send mail error', ', '.join(e.args))

    def verify_registration(self, params_signer, template_config, email=None, is_background=True):
        if email is None:
            email_field = get_user_setting('EMAIL_FIELD')
            email = getattr(self.user, email_field)
        body_template = get_template(template_config['body'])
        html_template = get_template(template_config['html'])
        subject_template = get_template(template_config['subject'])
        body_context = {
            'user': self.user,
            'email': email,
            'username': self.username,
            'login_name': self.login_name,
            'verification_url': params_signer.get_url(),
        }
        body_context.update(self.base_context)
        subject = subject_template.render(body_context).strip()
        body_context['subject'] = subject.split('] ')[1]
        body = body_template.render(body_context)
        msg_html = html_template.render(body_context)
        self.send_email(subject=subject, body=body, html=msg_html, receiver=[email], is_background=is_background)
