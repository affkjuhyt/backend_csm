import logging

from django.conf import settings
from django.db import models

from apps.vadmin.utils.base_models import BaseTimeStampModel
from groups.models import Group

logger = logging.getLogger(__name__.split('.')[0])


class PostGroup(BaseTimeStampModel):
    ENABLE = 1
    DISABLE = 0

    STATUS_POST_GROUP = (
        (ENABLE, 1),
        (DISABLE, 0)
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s",
        null=True
    )
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000, null=True, blank=True)
    like_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS_POST_GROUP, default=ENABLE, verbose_name='status')
    image_url = models.CharField(max_length=1000, null=True, blank=True, verbose_name='image_url')

    class Meta:
        verbose_name = 'PostGroup'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.group.name}" + " + " + f"{self.user.username}"
