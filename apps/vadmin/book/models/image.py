import logging

from django.db import models
from .chapter import Chapter

# from post.models import Post

from ...op_drf.models import CoreModel
from ...post.models.post import PostGroup

logger = logging.getLogger(__name__.split('.')[0])


class Image(CoreModel):
    post = models.ForeignKey(PostGroup, null=True, blank=True, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, null=True, blank=True, on_delete=models.CASCADE)
    image = models.FileField(
        upload_to='books/%Y/%m/%d',
        null=True
    )

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.id}"
