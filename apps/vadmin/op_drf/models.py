from django.conf import settings
from django.db import models
from django.db.models import SET_NULL

from .fields import CreateDateTimeField, DescriptionField, ModifierCharField, UpdateDateTimeField


class BaseModel(models.Model):

    description = DescriptionField()
    update_datetime = UpdateDateTimeField()
    create_datetime = CreateDateTimeField()

    class Meta:
        abstract = True
        verbose_name = 'Basic model'
        verbose_name_plural = verbose_name


class CoreModel(models.Model):
    """
    Mô hình mô hình trừu tượng tiêu chuẩn cốt lõi, có thể được kế thừa và sử dụng trực tiếp
    Thêm trường kiểm toán, khi ghi đè các trường, không được sửa đổi tên trường, bạn phải thống nhất tên trường kiểm tra
    """
    description = DescriptionField()
    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name='creator_query', null=True,
                                verbose_name='user_create', on_delete=SET_NULL, db_constraint=False)
    modifier = ModifierCharField()
    dept_belong_id = models.CharField(max_length=64, verbose_name="Data attribution department", null=True, blank=True)
    update_datetime = UpdateDateTimeField()
    create_datetime = CreateDateTimeField()

    class Meta:
        abstract = True
        verbose_name = 'Mô hình cốt lõi'
        verbose_name_plural = verbose_name


class BaseTimeStampModel(models.Model):
    dept_belong_id = models.CharField(max_length=64, verbose_name="Data attribution department", null=True, blank=True)
    update_datetime = UpdateDateTimeField()
    create_datetime = CreateDateTimeField()

    class Meta:
        abstract = True
