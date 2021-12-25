import logging

from django.db import models

from apps.vadmin.utils.base_models import BaseTimeStampModel

logger = logging.getLogger(__name__.split('.')[0])


class Group(BaseTimeStampModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    post_count = models.IntegerField(default=0)
    member_count = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='groups/avatar/%Y/%m/%d/', null=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name='description')
    # is_enable = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.name
