import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views.generic import detail
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_registration.exceptions import BadRequest
from rest_framework_jwt.settings import api_settings

from groups.models import GroupUser, Group
from groups.serializers import GroupSerializer
from userprofile.models import UserFollowing
from userprofile.serializers.user_profile import UserProfilePublicSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from application.authentications import BaseUserJWTAuthentication
from apps.vadmin.permission.models import UserProfile
from userprofile.serializers import UserProfileSerializer

logger = logging.getLogger(__name__.split('.')[0])

User = get_user_model()


class UserProfileView(ReadOnlyModelViewSet):
    serializer_class = UserProfilePublicSerializer
    permission_classes = [AllowAny]
    filter_fields = []
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        return User.objects.filter()


class UserPublicView(ReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    authentication_classes = [BaseUserJWTAuthentication]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        return User.objects.filter()

    @action(detail=False, methods=['get'], url_path='user_info')
    def get_user_info(self, request, *args, **kwargs):
        user = self.request.user
        user_serializer = UserProfileSerializer(user)
        return Response(user_serializer.data)

    @action(detail=True, methods=['post'], url_path='follow')
    def post_follow(self, request, *args, **kwargs):
        user = self.request.user
        user_following = self.get_object()
        user_follow = UserFollowing.objects.filter(user_id=user.id).filter(
            following_user_id_id=user_following.id).first()
        if user_follow is None:
            u_follow = UserFollowing.objects.create(user_id=user, following_user_id=user_following)
            u_follow.save()

            return Response("Follow successfully!", status=status.HTTP_200_OK)
        else:
            user_follow.delete()
            return Response("Unfollow successfully!", status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='list_groups')
    def get_list_groups(self, request, *args, **kwargs):
        user = self.request.user
        # breakpoint()
        group_user = GroupUser.objects.filter(user=user).values_list('group')
        groups = Group.objects.filter(pk__in=group_user)
        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(groups, request)
        list_comments = GroupSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(list_comments.data)


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
