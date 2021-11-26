import logging

from django.conf import settings
from django.db import models

from apps.vadmin.book.models import Book
from apps.vadmin.op_drf.models import BaseTimeStampModel

logger = logging.getLogger(__name__.split('.')[0])


class FollowBook(BaseTimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Follow book'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.id}"
