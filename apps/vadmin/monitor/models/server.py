from django.db import models
from django.db.models import CharField

from apps.vadmin.op_drf.fields import UpdateDateTimeField, CreateDateTimeField


class Server(models.Model):
    name = CharField(max_length=256, verbose_name='Tên máy chủ', null=True, blank=True)
    ip = CharField(max_length=32, verbose_name="Địa chỉ ip")
    os = CharField(max_length=32, verbose_name="Hệ điều hành")
    remark = CharField(max_length=256, verbose_name="Nhận xét", null=True, blank=True)
    update_datetime = UpdateDateTimeField()
    create_datetime = CreateDateTimeField()

    class Meta:
        verbose_name = 'Thông tin máy chủ'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name and self.ip}"
