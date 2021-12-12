import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from apps.vadmin.utils.base_models import BaseTimeStampModel

User = get_user_model()

logger = logging.getLogger(__name__.split('.')[0])


class HistorySearch(BaseTimeStampModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s"
    )
    text = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return "%s" % self.id
