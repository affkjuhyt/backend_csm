from django.db.models import CharField, ForeignKey, CASCADE

from apps.vadmin.op_drf.models import CoreModel


class Monitor(CoreModel):
    cpu_num = CharField(max_length=8, verbose_name='CPU')
    cpu_sys = CharField(max_length=8, verbose_name='CPU')
    mem_num = CharField(max_length=32, verbose_name='Mem(KB)')
    mem_sys = CharField(max_length=32, verbose_name='MemSys(KB)')
    seconds = CharField(max_length=32, verbose_name='Seconds')
    server = ForeignKey(to='monitor.Server', on_delete=CASCADE, verbose_name="server", db_constraint=False)

    class Meta:
        verbose_name = 'Monitor'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.server and self.server.name and self.server.ip}"
