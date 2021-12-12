import logging

from django.conf import settings
from django.db import models

from books.models import Book
from apps.vadmin.utils.base_models import BaseTimeStampModel

logger = logging.getLogger(__name__.split('.')[0])


class FollowBook(BaseTimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.id
