import logging

from django.db import models
from .book import Book

from apps.vadmin.utils.base_models import BaseTimeStampModel

logger = logging.getLogger(__name__.split('.')[0])


class Tag(BaseTimeStampModel):
    name = models.CharField(max_length=40, null=False, verbose_name="name")

    def __str__(self):
        return "%s" % self.name


class TagBook(BaseTimeStampModel):
    tag = models.ForeignKey(Tag, null=False, on_delete=models.CASCADE, blank=True, verbose_name="tag")
    book = models.ForeignKey(Book, null=False, on_delete=models.CASCADE, blank=True, verbose_name="book")

    def __str__(self):
        return "%s" % self.id

