from django.contrib import admin

from apps.vadmin.monitor.models import Server, Monitor


class ServersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ip', 'os', 'remark')
    search_fields = ['name']
    raw_id_fields = []
    # list_filter = ['book']


class MonitorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'cpu_num', 'cpu_sys', 'mem_num', 'mem_sys')
    search_fields = ['server']
    raw_id_fields = []


admin.site.register(Monitor, MonitorsAdmin)
admin.site.register(Server, ServersAdmin)
