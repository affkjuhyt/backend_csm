import logging

from django.db import models

from apps.vadmin.op_drf.models import BaseTimeStampModel

logger = logging.getLogger(__name__.split('.')[0])


class Profile(BaseTimeStampModel):
    ADMIN = 'admin'
    VIP = 'vip'
    NORMAL = 'normal'

    MALE = 'male'
    FEMALE = 'female'

    USER_TYPES = (
        (ADMIN, 'Admin'),
        (VIP, 'Vip'),
        (NORMAL, 'Normal')
    )

    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    email = models.CharField(max_length=40, null=False, blank=False)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, default=MALE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default=NORMAL)
    coin = models.IntegerField(default=0)
    point = models.IntegerField(default=1)
    avatar = models.ImageField(upload_to='userprofile/%Y/%m/%d', null=True, blank=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.full_name}"
