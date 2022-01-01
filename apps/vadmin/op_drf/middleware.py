import json
import logging
import os

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from apps.vadmin.op_drf.response import ErrorJsonResponse
from apps.vadmin.permission.models import Menu
from apps.vadmin.system.models import OperationLog
from apps.vadmin.utils.request_util import get_request_ip, get_request_data, get_request_path, get_browser, get_os, \
    get_login_location, get_request_canonical_path, get_request_user, get_verbose_name

logger = logging.getLogger(__name__)


class ApiLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.enable = getattr(settings, 'API_LOG_ENABLE', None) or False
        self.methods = getattr(settings, 'API_LOG_METHODS', None) or set()

    @classmethod
    def __handle_request(cls, request):
        request.request_ip = get_request_ip(request)
        request.request_data = get_request_data(request)
        request.request_path = get_request_path(request)

    @classmethod
    def __handle_response(cls, request, response):
        body = getattr(request, 'request_data', {})
        if isinstance(body, dict) and body.get('password', ''):
            body['password'] = '*' * len(body['password'])
        if not hasattr(response, 'data') or not isinstance(response.data, dict):
            response.data = {}
        if not response.data and response.content:
            try:
                content = json.loads(response.content.decode())
                response.data = content if isinstance(content, dict) else {}
            except:
                pass
        user = get_request_user(request)
        info = {
            'request_ip': getattr(request, 'request_ip', 'unknown'),
            'creator': user if not isinstance(user, AnonymousUser) else None,
            'dept_belong_id': getattr(request.user, 'dept_id', None),
            'request_method': request.method,
            'request_path': request.request_path,
            'request_body': body,
            'response_code': response.data.get('code'),
            'request_location': get_login_location(request),
            'request_os': get_os(request),
            'request_browser': get_browser(request),
            'request_msg': request.session.get('request_msg'),
            'status': True if response.data.get('code') in [200, 204] else False,
            'json_result': {"code": response.data.get('code'), "msg": response.data.get('msg')},
            'request_modular': request.session.get('model_name'),
        }
        log = OperationLog(**info)
        log.save()

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func, 'cls') and hasattr(view_func.cls, 'queryset'):
            request.session['model_name'] = get_verbose_name(view_func.cls.queryset)
        return

    def process_request(self, request):
        self.__handle_request(request)

    def process_response(self, request, response):
        if self.enable:
            if self.methods == 'ALL' or request.method in self.methods:
                self.__handle_response(request, response)
        return response


class PermissionModeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        return

    def has_interface_permission(self, request, method, view_path, user=None):
        interface_dict = Menu.get_interface_dict()
        if not view_path in interface_dict.get(method, []):
            return 10
        if user.is_superuser or (hasattr(user, 'role') and user.role.filter(status='1', admin=True).count()):
            return 20
        if view_path in user.get_user_interface_dict.get(method, []):
            return 30
        return -10

    def process_view(self, request, view_func, view_args, view_kwargs):
        white_list = ['/admin/logout/', '/admin/login/', '/admin/api-auth/login/']
        if os.getenv('DEMO_ENV') and not request.method in ['GET', 'OPTIONS'] and request.path not in white_list:
            return ErrorJsonResponse(data={}, msg=f'Demo mode, operation is not allowed!')

        if not settings.INTERFACE_PERMISSION:
            return
        user = get_request_user(request)

        if user and not isinstance(user, AnonymousUser):
            method = request.method.upper()
            if method == 'GET':
                return
            view_path = get_request_canonical_path(request, *view_args, **view_kwargs)
            auth_code = self.has_interface_permission(request, method, view_path, user)
            logger.info(f"[{user.username}] {method}:{view_path}, Authority authentication:{auth_code}")
            if auth_code >= 0:
                return
            return ErrorJsonResponse(data={}, msg=f'No interface access!')

    def process_response(self, request, response):
        return response
