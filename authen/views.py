
import logging

import requests
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from validate_email import validate_email

from application import settings
from apps.vadmin.permission.models import UserProfile
from apps.vadmin.op_drf.response import ErrorResponse, SuccessResponse

User = get_user_model()

logger = logging.getLogger(__name__.split('.')[0])

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

FACEBOOK_DEBUG_TOKEN_URL = "https://graph.facebook.com/debug_token"
FACEBOOK_ACCESS_TOKEN_URL = "https://graph.facebook.com/v7.0/oauth/access_token"
FACEBOOK_URL = "https://graph.facebook.com/"


class GoogleView(APIView):
    def post(self, request):
        payload = {'access_token': request.data.get("token")}
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        try:
            user = User.objects.get(last_name=data['email'])
        except User.DoesNotExist:
            user = User()
            user.last_name = data['email']
            user.username = data['email']
            user.password = make_password(BaseUserManager().make_random_password())
            user.save()

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response = {}
        response["user_id"] = user.id
        response['username'] = user.username
        response['access_token'] = str(token)
        return Response(response)


class FacebookView(APIView):
    def post(self, request):
        user_info_url = FACEBOOK_URL + request.data.get("id")
        print(request.data.get("id"), request.data.get("token"))
        user_info_payload = {
            "access_token": request.data.get("token"),
        }

        user_info_request = requests.get(user_info_url, params=user_info_payload)
        user_info_response = json.loads(user_info_request.text)

        try:
            user = User.objects.get(last_name=user_info_response["id"])
        except User.DoesNotExist:
            user = User()
            user.last_name = user_info_response["id"]
            user.username = user_info_response["id"]
            user.password = make_password(BaseUserManager().make_random_password())
            user.save()

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response = {}
        response["user_id"] = user.id
        response["username"] = user.username
        response["access_token"] = str(token)
        return Response(response)


class AppleView(APIView):
    def post(self, request):
        if not request.data:
            return Response({'Error': "Please provide user_id"}, status=status.HTTP_400_BAD_REQUEST)

        user_name = request.data.get("user_id")

        try:
            user = User.objects.get(last_name=user_name)
        except User.DoesNotExist:
            user = User()
            user.last_name = user_name
            user.username = user_name
            user.password = make_password(BaseUserManager().make_random_password())
            user.save()

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response = {}
        response["username"] = user.username
        response["user_id"] = user.id
        response["access_token"] = str(token)
        return Response(response, status=status.HTTP_200_OK)


class LoginAPI(APIView):
    def post(self, request):
        if not request.data:
            return Response({'Error': "Please provide username/password"}, status=status.HTTP_400_BAD_REQUEST)

        username = request.data['username']
        password = request.data['password']
        response = {}
        if validate_email(username):
            email = request.data['username']
            try:
                user_profile = UserProfile.objects.filter(email=email).first()
                user = User.objects.filter(Q(id=user_profile.user.id) | Q(password=password)).first()
            except:
                return Response({'Error': "Invalid username/password"}, status=status.HTTP_400_BAD_REQUEST)

            if user:
                payload = jwt_payload_handler(user)
                jwt_token = jwt_encode_handler(payload)

                response["email"] = user.email
                response["access_token"] = jwt_token

            return Response(response, status=status.HTTP_200_OK)
        else:
            phone_number = request.data['username']
            try:
                user_profile = UserProfile.objects.filter(phone_number=phone_number).first()
                user = User.objects.filter(Q(id=user_profile.id) | Q(password=password)).first()
            except:
                return Response({'Error': "Invalid username/password"}, status=status.HTTP_400_BAD_REQUEST)

            if user:
                payload = jwt_payload_handler(user)
                jwt_token = jwt_encode_handler(payload)

                response["email"] = user.email
                response["access_token"] = jwt_token

            return Response(response, status=status.HTTP_200_OK)


# class LoginAdminAPI(ObtainJSONWebToken):
#     JWT_AUTH_COOKIE = ''
#     prefix = settings.JWT_AUTH.get('JWT_AUTH_HEADER_PREFIX')
#     ex = settings.JWT_AUTH.get('JWT_EXPIRATION_DELTA')
#
#     def jarge_captcha(self, request):
#         if not base.CAPTCHA_STATE:
#             return True
#         idKeyC = request.data.get('idKeyC', None)
#         idValueC = request.data.get('idValueC', None)
#         if not idValueC:
#             raise GenException(message='Please enter the confirmation code')
#         try:
#             get_captcha = CaptchaStore.objects.get(hashkey=idKeyC)
#             if str(get_captcha.response).lower() == idValueC.lower():
#                 get_captcha.delete()
#                 return True
#         except:
#             pass
#         else:
#             if get_captcha: get_captcha.delete()
#             raise GenException(message='Please enter the confirmation code')
#
#     def save_login_infor(self, request, msg='', status=True, session_id=''):
#         User = get_user_model()
#         instance = LoginInfor()
#         instance.session_id = session_id
#         instance.browser = get_browser(request)
#         instance.ipaddr = get_request_ip(request)
#         instance.loginLocation = get_login_location(request)
#         instance.msg = msg
#         instance.os = get_os(request)
#         instance.status = status
#         instance.creator = request.user and User.objects.filter(username=request.data.get('username')).first()
#         instance.save()
#
#     def post(self, request, *args, **kwargs):
#         self.jarge_captcha(request)
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.object.get('user') or request.user
#             token = serializer.object.get('token')
#             response_data = jwt_response_payload_handler(token, user, request)
#             response = SuccessResponse(response_data)
#
#             if token:
#                 username = user.username
#                 session_id = jwt_get_session_id(token)
#                 key = f"{self.prefix}_{session_id}_{username}"
#                 if getattr(settings, "REDIS_ENABLE", False):
#                     cache.set(key, token, self.ex.total_seconds())
#                 self.save_login_infor(request, 'login not successfully', session_id=session_id)
#             if self.JWT_AUTH_COOKIE and token:
#                 expiration = (datetime.datetime.utcnow() + self.ex)
#                 response.set_cookie(self.JWT_AUTH_COOKIE,
#                                     token,
#                                     expires=expiration,
#                                     domain=settings.SESSION_COOKIE_DOMAIN,
#                                     httponly=False)
#             return response
#         self.save_login_infor(request, 'Login not successfully', False)
#         return ErrorResponse(data=serializer.errors, msg='username/password not correct')


class LogoutView(APIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    prefix = settings.JWT_AUTH.get('JWT_AUTH_HEADER_PREFIX', 'JWT')

    def post(self, request):
        user = request.user
        user.save()
        key = f"{self.prefix}_{user.username}"
        if getattr(settings, "REDIS_ENABLE", False):
            cache.delete(key)
        return SuccessResponse()
