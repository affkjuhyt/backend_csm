from django.db.models import CharField, ForeignKey, CASCADE

from apps.vadmin.op_drf.models import CoreModel


class SysFiles(CoreModel):
    dir_name = CharField(max_length=32, verbose_name='dir_name')
    sys_type_name = CharField(max_length=400, verbose_name='sys_type_name')
    type_name = CharField(max_length=32, verbose_name='type_name')
    total = CharField(max_length=32, verbose_name='total(KB)')
    disk_sys = CharField(max_length=32, verbose_name='disk_sys(KB)')
    monitor = ForeignKey(to='monitor.Monitor', on_delete=CASCADE, verbose_name="monitor", db_constraint=False)

    class Meta:
        verbose_name = 'SysFiles'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.creator and self.creator.name}"
