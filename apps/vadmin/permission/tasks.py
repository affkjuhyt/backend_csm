import datetime
import logging

from captcha.models import CaptchaStore

from apps.vadmin.utils.decorators import BaseCeleryApp
from apps.vadmin.op_drf.response import SuccessResponse

logger = logging.getLogger(__name__)
@BaseCeleryApp(name='apps.vadmin.permission.tasks.clear_invalid_captcha')
def clear_invalid_captcha():
    """
    :return:
    """
    queryset = CaptchaStore.objects.filter(expiration__lt=datetime.datetime.now())
    msg = f"Successfully deleted {queryset.count()} Invalid verification code!"
    logger.info(msg)
    queryset.delete()
    return SuccessResponse(msg=msg)
