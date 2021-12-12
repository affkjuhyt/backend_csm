from django.contrib import admin

from collector.models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'created', 'user_id', 'content_id', 'event', 'session_id')
    search_fields = ['event', 'user_id']
    raw_id_fields = []


admin.site.register(Log, LogAdmin)
