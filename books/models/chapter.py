import logging

from django.db import models
from .book import Book

from apps.vadmin.utils.base_models import BaseTimeStampModel

logger = logging.getLogger(__name__.split('.')[0])


class Chapter(BaseTimeStampModel):
    book = models.ForeignKey(Book, null=True, on_delete=models.CASCADE)
    number = models.IntegerField(null=True)
    title = models.CharField(max_length=1000, null=False)
    thumbnail = models.ImageField(upload_to='books/%Y/%m/%d', null=True, blank=True)
    like_count = models.IntegerField(default=0)
    description = models.TextField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = 'chapter'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.id
