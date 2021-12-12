from django.contrib import admin

from filemedia.models import File, Video


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'file')
    search_fields = ['id']
    raw_id_fields = []
    list_filter = ['post']


admin.site.register(File, FileAdmin)


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'video')
    search_fields = ['id']
    raw_id_fields = []
    list_filter = ['post']


admin.site.register(Video, VideoAdmin)
