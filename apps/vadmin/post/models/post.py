import logging

from django.conf import settings
from django.db import models

# from group.models import Group
# from utils.base_models import BaseTimeStampModel

from apps.vadmin.op_drf.models import CoreModel

logger = logging.getLogger(__name__.split('.')[0])


class Post(CoreModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s"
    )
    # group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000, null=True, blank=True)
    like_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
