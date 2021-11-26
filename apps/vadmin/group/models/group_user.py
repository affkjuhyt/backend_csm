import logging

from django.conf import settings
from django.db import models

# from utils.base_models import BaseTimeStampModel
from apps.vadmin.group.models import Group
from apps.vadmin.op_drf.models import CoreModel

logger = logging.getLogger(__name__.split('.')[0])


class GroupUser(CoreModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s"
    )

    class Meta:
        verbose_name = 'GroupUser'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.id
