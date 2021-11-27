from django.contrib import admin

from apps.vadmin.post.models import PostGroup


class PostGroupsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'group', 'content', 'like_count', 'share_count')
    search_fields = ['user']
    raw_id_fields = []
    list_filter = ['group', 'user']


admin.site.register(PostGroup, PostGroupsAdmin)
