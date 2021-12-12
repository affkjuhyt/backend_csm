import logging

from django.db import models

from apps.vadmin.utils.base_models import BaseTimeStampModel

logger = logging.getLogger(__name__.split('.')[0])


class Group(BaseTimeStampModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    post_count = models.IntegerField(default=0)
    member_count = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % self.name
