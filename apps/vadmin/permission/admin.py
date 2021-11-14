from django.contrib import admin

from apps.vadmin.permission.models import Menu


class MenusAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'parentId', 'menuType', 'icon', 'name', 'orderNum', 'isFrame', 'web_path', 'component_path',
        'interface_path', 'interface_method', 'perms', 'status', 'visible', 'isCache')
    search_fields = ['title', 'author']
    raw_id_fields = []
    list_filter = ['parentId', 'orderNum', 'status']


admin.site.register(Menu, MenusAdmin)
