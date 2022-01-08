import logging

from django.db import models

from apps.vadmin.utils.base_models import BaseTimeStampModel

logger = logging.getLogger(__name__.split('.')[0])


class VulgarWord(BaseTimeStampModel):
    word = models.CharField(max_length=100)
    re_word = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'vulgar'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.id