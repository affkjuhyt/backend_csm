#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  base_auth.py

from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.translation import ugettext as _

from apps.vadmin.utils import jwt


class BaseUserJWTAuthentication(JSONWebTokenAuthentication):

    def authenticate(self, request):
        result = super(BaseUserJWTAuthentication, self).authenticate(request)
        return result

    def get_jwt_value(self, request):
        '''
            JWT from appointment app does not include "JWT" prefix
        '''
        auth = get_authorization_header(request).split()
        if not auth:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) > 1:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[0]

    def get_user(self, payload):
        User = get_user_model()
        user_info = jwt.from_payload_to_user_info(payload)
        user_name = payload.get('username', None)
        user_id = payload.get('user_id', None)
        email = payload.get('email', None)

        user, _ = User.objects.get_or_create(**user_info)
        return user

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
        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user
