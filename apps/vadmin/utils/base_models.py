#!/usr/bin/python
# -*- coding: utf-8 -*-
import uuid

from django.conf import settings
from django.db import models
from django.db.models import SET_NULL


class BaseTimeStampModel(models.Model):
    date_added = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class BaseUserModel(BaseTimeStampModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s"
    )

    class Meta:
        abstract = True


class BaseForeignKeyUserModel(BaseTimeStampModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class BaseModel(BaseTimeStampModel):
    class Meta:
        abstract = True


class BaseUUIDModel(BaseTimeStampModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class CoreModel(models.Model):
    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name='creator_query', null=True, on_delete=SET_NULL, db_constraint=False)  # 创建者
    dept_belong_id = models.CharField(max_length=100, null=True, blank=True)
    update_datetime = models.DateTimeField(auto_now=True)
    create_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
