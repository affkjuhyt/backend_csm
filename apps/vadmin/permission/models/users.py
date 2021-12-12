import logging
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.cache import cache
from django.db import models
from django.db.models import CASCADE

from apps.vadmin.utils.base_models import CoreModel

# User = get_user_model()

logger = logging.getLogger(__name__.split('.')[0])


class UserProfile(AbstractUser, CoreModel):
    MALE = 'male'
    FEMALE = 'female'

    LEVEL0 = '0'
    LEVEL1 = '1'
    LEVEL2 = '2'
    LEVEL3 = '3'
    LEVEL4 = '4'
    LEVEL5 = '5'

    LEVEL = (
        (LEVEL0, '0'),
        (LEVEL1, '1'),
        (LEVEL2, '2'),
        (LEVEL3, '3'),
        (LEVEL4, '4'),
        (LEVEL5, '5'),
    )

    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    objects = UserManager()
    email = models.CharField(max_length=255, null=False, blank=False, verbose_name="email")
    full_name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True, db_index=True, verbose_name='username')
    secret = models.CharField(max_length=255, default=uuid4, verbose_name='secret')
    phone_number = models.CharField(max_length=20, verbose_name="mobile", null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, default=MALE)
    name = models.CharField(max_length=40, verbose_name="name")
    level = models.CharField(max_length=20, choices=LEVEL, default=LEVEL3)
    coin = models.IntegerField(default=0)
    point = models.IntegerField(default=1)
    avatar = models.ImageField(upload_to='userprofile/%Y/%m/%d', null=True, blank=True, verbose_name="avatar")
    remark = models.TextField(verbose_name="remark", null=True)
    user_type = models.IntegerField(default=0, verbose_name="user_type")
    # post = models.ManyToManyField(to='permission.Post', verbose_name='post', db_constraint=False)
    role = models.ManyToManyField(to='permission.Role', verbose_name='role', db_constraint=False)
    dept = models.ForeignKey(to='permission.Dept', verbose_name='dept', on_delete=CASCADE, db_constraint=False,
                             null=True,
                             blank=True)

    @property
    def get_user_interface_dict(self):
        interface_dict = cache.get(f'permission_interface_dict_{self.username}', {}) if \
            getattr(settings, "REDIS_ENABLE", False) else {}
        if not interface_dict:
            for ele in self.role.filter(status='1', menu__status='1').values('menu__interface_path',
                                                                             'menu__interface_method').distinct():
                interface_path = ele.get('menu__interface_path')
                if interface_path is None or interface_path == '':
                    continue
                if ele.get('menu__interface_method') in interface_dict:
                    interface_dict[ele.get('menu__interface_method', '')].append(interface_path)
                else:
                    interface_dict[ele.get('menu__interface_method', '')] = [interface_path]
            if getattr(settings, "REDIS_ENABLE", False):
                cache.set(f'permission_interface_dict_{self.username}', interface_dict, 84600)
        return interface_dict

    @property
    def delete_cache(self):
        if not getattr(settings, "REDIS_ENABLE", False): return ""
        return cache.delete(f'permission_interface_dict_{self.username}')

    class Meta:
        abstract = settings.AUTH_USER_MODEL != 'permission.UserProfile'
        verbose_name = 'Quan ly nguoi dung'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.name:
            return f"{self.username}({self.name})"
        return f"{self.username}"
