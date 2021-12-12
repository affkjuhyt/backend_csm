from django.contrib import admin

from bookcase.models import History


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'chapter', 'hide']
    search_fields = ['user']
    raw_id_fields = []
    list_filter = ['user']


admin.site.register(History, HistoryAdmin)
