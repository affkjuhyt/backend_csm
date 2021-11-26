import logging

from django.db import models

# from utils.base_models import BaseTimeStampModel

from apps.vadmin.op_drf.models import CoreModel

logger = logging.getLogger(__name__.split('.')[0])


class Group(CoreModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    post_count = models.IntegerField(default=0)
    member_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name
