import logging

from django.db import models

from apps.vadmin.op_drf.models import CoreModel

logger = logging.getLogger(__name__.split('.')[0])


class Book(CoreModel):
    PROCESSING = 'processing'
    SUSPENSION = 'suspension'
    NEW = 'new'
    FULL = 'full'

    STAR1 = 1
    STAR2 = 2
    STAR3 = 3
    STAR4 = 4
    STAR5 = 5

    STAR_STATUS = (
        (STAR1, '1'),
        (STAR2, '2'),
        (STAR3, '3'),
        (STAR4, '4'),
        (STAR5, '5'),
    )

    BOOK_STATUS = (
        (PROCESSING, 'Processing'),
        (SUSPENSION, 'Suspension'),
        (NEW, 'New'),
        (FULL, 'Full')
    )

    title = models.CharField(max_length=1000, null=False, verbose_name='name_book')
    thumbnail = models.ImageField(upload_to='books/%Y/%m/%d/', null=True, blank=True, verbose_name='thumbnail')
    author = models.CharField(max_length=300, null=True, verbose_name='author')
    status = models.CharField(max_length=20, choices=BOOK_STATUS, default=NEW, verbose_name='status')
    type = models.CharField(max_length=20, verbose_name='type')
    like_count = models.IntegerField(default=0, verbose_name='like_count')
    view_count = models.IntegerField(default=0, verbose_name='view_count')
    star = models.IntegerField(choices=STAR_STATUS, default=STAR1, verbose_name='star')
    is_enable = models.BooleanField(default=False, verbose_name='is_enable')
    is_vip = models.BooleanField(default=False, verbose_name='is_vip')
    is_full = models.BooleanField(default=False, verbose_name='is_full')
    is_suggest = models.BooleanField(default=False, verbose_name='is_suggest')

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.title}"
