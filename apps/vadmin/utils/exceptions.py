import logging
import traceback

from rest_framework import exceptions
from rest_framework.views import set_rollback

from apps.vadmin.op_drf.response import ErrorResponse

logger = logging.getLogger(__name__)

from rest_framework.exceptions import APIException as DRFAPIException, AuthenticationFailed


class APIException(Exception):

    def __init__(self, code=201, message='API exception', args=('API exception',)):
        self.args = args
        self.code = code
        self.message = message

    def __str__(self):
        return self.message


class GenException(APIException):
    pass


class FrameworkException(Exception):

    def __init__(self, message='Frame exception', *args: object, **kwargs: object) -> None:
        super().__init__(*args, )
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class JWTAuthenticationFailedException(APIException):

    def __init__(self, code=201, message=None, args=('Abnormal',)):
        if not message:
            message = 'JWT authentication failed!'
        super().__init__(code, message, args)


def op_exception_handler(ex, context):
    """
    :param ex:
    :param context:
    :return:
    """
    msg = ''
    code = '201'

    if isinstance(ex, AuthenticationFailed):
        code = 401
        msg = ex.detail
    elif isinstance(ex, DRFAPIException):
        set_rollback()
        msg = ex.detail
    elif isinstance(ex, exceptions.APIException):
        set_rollback()
        msg = ex.detail
    elif isinstance(ex, Exception):
        logger.error(traceback.format_exc())
        msg = str(ex)
    return ErrorResponse(msg=msg, code=code)
