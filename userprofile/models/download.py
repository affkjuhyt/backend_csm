import logging

from django.conf import settings
from django.db import models

from books.models import Chapter
from apps.vadmin.utils.base_models import BaseTimeStampModel

logger = logging.getLogger(__name__.split('.')[0])


class DownLoadBook(BaseTimeStampModel):
    PROCESSING = 'processing'
    SUCCESS = 'success'
    ERROR = 'error'
    NOT_DOWNLOAD = 'not_download'

    DOWNLOAD_STATUS = (
        (PROCESSING, 'Processing'),
        (SUCCESS, 'Success'),
        (ERROR, 'Error'),
        (NOT_DOWNLOAD, 'Not download')
    )

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=DOWNLOAD_STATUS, default=PROCESSING)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s"
    )

    def __str__(self):
        return "%s" % self.id
