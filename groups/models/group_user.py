import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from apps.vadmin.utils.base_models import BaseTimeStampModel
from groups.models import Group

User = get_user_model()

logger = logging.getLogger(__name__.split('.')[0])


class GroupUser(BaseTimeStampModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s"
    )

    def __str__(self):
        return "%s" % self.id
