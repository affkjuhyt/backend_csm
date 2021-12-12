import datetime
import logging

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import ugettext as _
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_registration.api.serializers import DefaultSendResetPasswordLinkSerializer
from rest_registration.api.views.change_password import ChangePasswordSerializer
from rest_registration.api.views.reset_password import ResetPasswordSigner
from rest_registration.exceptions import BadRequest, UserNotFound
from rest_registration.settings import registration_settings
from rest_registration.utils.responses import get_ok_response

from authen.serializers import ResetPasswordSerializer
# from root import settings
from application.authentications import BaseUserJWTAuthentication
from apps.vadmin.utils.email import EmailUserNotification

logger = logging.getLogger(__name__.split('.')[0])


class PasswordViewSet(viewsets.GenericViewSet):
    @action(
        detail=False,
        methods=['posts'],
        url_path='change',
        serializer_class=ChangePasswordSerializer,
        authentication_classes=[BaseUserJWTAuthentication, ]
    )
    def change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['password'])
        user.userprofile.last_update_password = datetime.datetime.utcnow()
        user.userprofile.save()
        user.save()
        return get_ok_response(_('Password changed successfully'))

    @action(detail=False, methods=['post'], url_path='forgot', serializer_class=DefaultSendResetPasswordLinkSerializer)
    def forgot(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login = serializer.validated_data['login']

        user_query = (Q(username=login) | Q(email=login)) & Q(is_active=True)
        user = User.objects.filter(user_query).first()
        if not user:
            raise UserNotFound()

        signer = ResetPasswordSigner({
            'user_id': user.pk,
        }, request=request)

        template_config = (
            registration_settings.RESET_PASSWORD_VERIFICATION_EMAIL_TEMPLATES)
        logger.info(request.get_host())
        EmailUserNotification(user=user, host=request.get_host()).verify_registration(
            params_signer=signer,
            template_config=template_config
        )

        return get_ok_response('Reset link sent')

    @action(detail=False, methods=['post'], url_path='reset', serializer_class=ResetPasswordSerializer)
    def reset(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return get_ok_response('Reset password success')
