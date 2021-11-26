from django.db.models import IntegerField, BooleanField, CharField, TextField, ManyToManyField

from apps.vadmin.op_drf.models import CoreModel


class Role(CoreModel):
    DATASCOPE_CHOICES = (
        ('1', "Tất cả các quyền dữ liệu"),
        ('2', "Quyền đối với dữ liệu tùy chỉnh"),
        ('3', "Cơ quan dữ liệu của bộ phận này"),
        ('4', "Cơ quan dữ liệu của bộ phận này trở xuống"),
        ('5', "Chỉ truy cập dữ liệu cá nhân"),
    )
    roleName = CharField(max_length=64, verbose_name="roleName")
    roleKey = CharField(max_length=64, verbose_name="roleKey")
    roleSort = IntegerField(verbose_name="roleSort")
    status = CharField(max_length=8, verbose_name="status")
    admin = BooleanField(default=False, verbose_name="admin")
    dataScope = CharField(max_length=8, default='1', choices=DATASCOPE_CHOICES, verbose_name="dataScope", )
    remark = TextField(verbose_name="remark", help_text="remark", null=True, blank=True)
    dept = ManyToManyField(to='permission.Dept', verbose_name='dept', db_constraint=False)
    menu = ManyToManyField(to='permission.Menu', verbose_name='menu', db_constraint=False)

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.roleName}"
