import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_registration.exceptions import BadRequest
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from application.authentications import BaseUserJWTAuthentication
from apps.vadmin.permission.models import UserProfile
from userprofile.serializers import UserProfileSerializer

logger = logging.getLogger(__name__.split('.')[0])

User = get_user_model()


class UserPublicView(ReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    authentication_classes = [BaseUserJWTAuthentication]
    filter_fields = []
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        return User.objects.filter()

    @action(detail=False, methods=['get'], url_path='user_info')
    def get_user_info(self, request, *args, **kwargs):
        user = self.request.user
        # user_profile = User.objects.filter(id=user.id).first()
        return Response(user.data)


class UpdateInfo(ReadOnlyModelViewSet):
    authentication_classes = [BaseUserJWTAuthentication]
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response({'Error': "Please provide username/password"}, status=status.HTTP_400_BAD_REQUEST)

        username = request.data['username']
        password = request.data['password']

        username = username.lower()
        if User.objects.filter(username=username).exists():
            return Response({'Error': 'Username already exists'})
        else:
            user = User.objects.filter(id=request.user.id).first()
            user.username = username
            try:
                validate_password(password, user=user)
            except ValidationError as exc:
                raise BadRequest(exc.messages[0])

            user.set_password(password)
            user.save()

            if user:
                payload = jwt_payload_handler(user)
                jwt_token = jwt_encode_handler(payload)

                response = {}
                response["access_token"] = jwt_token

            return Response(response, status=status.HTTP_200_OK)