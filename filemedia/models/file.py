import logging

from django.db import models

from posts.models import PostGroup
from apps.vadmin.utils.base_models import BaseTimeStampModel

logger = logging.getLogger(__name__.split('.')[0])


class File(BaseTimeStampModel):
    post = models.ForeignKey(PostGroup, null=True, blank=True, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to='books/%Y/%m/%d',
        null=True
    )

    def __str__(self):
        return "%s" % self.id
