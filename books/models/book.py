import logging

from django.db import models

from apps.vadmin.utils.base_models import BaseTimeStampModel

logger = logging.getLogger(__name__.split('.')[0])


class Book(BaseTimeStampModel):
    MALE = 'male'
    FEMALE = 'female'

    PROCESSING = 'processing'
    SUSPENSION = 'suspension'
    NEW = 'new'
    FULL = 'full'

    COMIC = 'comic'
    NOVEL = 'novel'

    STAR1 = 1
    STAR2 = 2
    STAR3 = 3
    STAR4 = 4
    STAR5 = 5

    SEX_TYPES = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )

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

    BOOK_TYPES = (
        (COMIC, 'Comic'),
        (NOVEL, 'Novel')
    )

    title = models.CharField(max_length=1000, null=False)
    thumbnail = models.ImageField(upload_to='books/%Y/%m/%d/', null=True, blank=True)
    description = models.CharField(max_length=2000, null=True)
    author = models.CharField(max_length=300, null=True)
    sex = models.CharField(max_length=20, choices=SEX_TYPES, default=MALE)
    status = models.CharField(max_length=20, choices=BOOK_STATUS, default=NEW)
    type = models.CharField(max_length=20, choices=BOOK_TYPES, default=COMIC)
    like_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    star = models.IntegerField(choices=STAR_STATUS, default=STAR1)
    is_enable = models.BooleanField(default=False)
    is_vip = models.BooleanField(default=False)
    is_full = models.BooleanField(default=False)
    is_suggest = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.title
