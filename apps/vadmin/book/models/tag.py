import logging

from django.db import models
from .book import Book
from ...op_drf.models import BaseTimeStampModel

logger = logging.getLogger(__name__.split('.')[0])


class Tag(BaseTimeStampModel):
    name = models.CharField(max_length=40, null=False, verbose_name="name")

    def __str__(self):
        return "%s" % self.name


class TagBook(BaseTimeStampModel):
    tag = models.ForeignKey(Tag, null=False, on_delete=models.CASCADE, verbose_name="tag", blank=True)
    book = models.ForeignKey(Book, null=False, on_delete=models.CASCADE, verbose_name="book", blank=True)

    def __str__(self):
        return "%s" % self.id

