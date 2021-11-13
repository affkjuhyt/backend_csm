import logging

from django.db import models

from apps.vadmin.book.models import Book
from apps.vadmin.op_drf.models import CoreModel

logger = logging.getLogger(__name__.split('.')[0])


class Chapter(CoreModel):
    book = models.ForeignKey(Book, null=True, on_delete=models.CASCADE, verbose_name="book")
    number = models.IntegerField(null=True, verbose_name='number')
    title = models.CharField(max_length=1000, null=False, verbose_name='title')
    thumbnail = models.ImageField(upload_to='books/%Y/%m/%d', null=True, blank=True, verbose_name='thumbnail')
    like_count = models.IntegerField(default=0, verbose_name='like_count')

    class Meta:
        verbose_name = 'chapter'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.title}"
