from rest_framework import exceptions
from django.utils.translation import ugettext as _
from application.authentications import BaseUserJWTAuthentication


class AdminUserJWTAuthentication(BaseUserJWTAuthentication):
    def authenticate_credentials(self, payload):
        """
            If there is no user_id, create a new one
        """
        user_id = payload.get('user_id')

        if not user_id:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = self.get_user(payload)
        except Exception:
            msg = _('Please log out and log in again.')
            raise exceptions.AuthenticationFailed(msg)

        if user.is_superuser:
            return user

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_staff:
            msg = _('User account is not staff.')
            raise exceptions.AuthenticationFailed(msg)

        return user
