from django.contrib import admin

from groups.models import Group, GroupUser


class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'post_count', 'member_count']
    search_fields = ['name']
    raw_id_fields = []


class GroupUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'user']
    search_fields = ['user']
    raw_id_fields = []
    list_filter = []


admin.site.register(GroupUser, GroupUserAdmin)
admin.site.register(Group, GroupAdmin)
