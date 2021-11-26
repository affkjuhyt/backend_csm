import logging

from django.conf import settings
from django.db import models

from apps.vadmin.group.models import Group
from apps.vadmin.op_drf.models import BaseTimeStampModel

logger = logging.getLogger(__name__.split('.')[0])


class PostGroup(BaseTimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s"
    )
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000, null=True, blank=True)
    like_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
