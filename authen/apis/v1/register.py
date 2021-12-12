import logging

from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_registration.api.views.register import RegisterSigner, VerifyRegistrationSerializer
from rest_registration.exceptions import BadRequest
from rest_registration.settings import registration_settings
from rest_registration.utils.responses import get_ok_response
from rest_registration.utils.users import get_user_setting, get_user_by_verification_id
from rest_registration.utils.verification import verify_signer_or_bad_request

from apps.vadmin.permission.models import UserProfile
from apps.vadmin.utils.common import full_name
from apps.vadmin.utils.email import EmailUserNotification

logger = logging.getLogger(__name__.split('.')[0])


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = registration_settings.REGISTER_SERIALIZER_CLASS

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kwargs = {}

        if registration_settings.REGISTER_VERIFICATION_ENABLED:
            verification_flag_field = get_user_setting('VERIFICATION_FLAG_FIELD')
            kwargs[verification_flag_field] = False
            email_field = get_user_setting('EMAIL_FIELD')
            if (email_field not in serializer.validated_data
                    or not serializer.validated_data[email_field]):
                raise BadRequest('User without email cannot be verified')
            if User.objects.filter(email=serializer.validated_data[email_field], is_active=True).exists():
                raise BadRequest('This email already exist.')

        user = serializer.save(**kwargs)

        output_serializer_class = registration_settings.REGISTER_OUTPUT_SERIALIZER_CLASS  # noqa: E501
        output_serializer = output_serializer_class(instance=user)
        user_data = output_serializer.data
        if registration_settings.REGISTER_VERIFICATION_ENABLED:
            signer = RegisterSigner({
                'user_id': user.pk,
            }, request=request)
            template_config = (
                registration_settings.REGISTER_VERIFICATION_EMAIL_TEMPLATES)
            EmailUserNotification(user=user, host=request.get_host()).verify_registration(
                params_signer=signer,
                template_config=template_config
            )

        logger.info(f'New user registered {user_data}')

        return Response(user_data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['posts'],
        url_path='verify',
        serializer_class=VerifyRegistrationSerializer,
        permission_classes=[]
    )
    def verify(self, request):
        logger.info('verify.data: ', request.data)
        if not registration_settings.REGISTER_VERIFICATION_ENABLED:
            raise Http404()
        serializer = VerifyRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        signer = RegisterSigner(data)
        verify_signer_or_bad_request(signer)

        verification_flag_field = get_user_setting('VERIFICATION_FLAG_FIELD')
        user = get_user_by_verification_id(data['user_id'], require_verified=False)
        if User.objects.filter(email=user.email, is_active=True).exists():
            raise BadRequest('This email already verified.')
        setattr(user, verification_flag_field, True)
        user.save()
        return get_ok_response('User verified successfully')
