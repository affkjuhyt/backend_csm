from django.contrib import admin

from apps.vadmin.group.models import Group, GroupUser


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'post_count', 'member_count', 'description', 'creator')
    search_fields = ['name']
    raw_id_fields = []
    list_filter = ['creator']


class GroupUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'group', 'user', 'description', 'creator'
    )
    search_fields = ['description']
    raw_id_fields = []
    list_filter = ['user']


admin.site.register(Group, GroupAdmin)
admin.site.register(GroupUser, GroupUserAdmin)
