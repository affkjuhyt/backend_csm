from django.contrib import admin

from apps.vadmin.monitor.models import Server


class ServersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ip', 'os', 'remark')
    search_fields = ['name']
    raw_id_fields = []
    # list_filter = ['book']


admin.site.register(Server, ServersAdmin)
