from django.contrib import admin

from userprofile.models import FollowBook, DownLoadBook, UserFollowing
from apps.vadmin.permission.models import UserProfile


# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'email', 'full_name', 'user_type', 'coin', 'level']
#     search_fields = ['full_name', 'email']
#     raw_id_fields = ['user']
#
#
# admin.site.register(UserProfile, UserProfileAdmin)


class FollowBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'status']
    search_fields = ['user', 'book']
    raw_id_fields = ['user']


admin.site.register(FollowBook, FollowBookAdmin)


class DownloadAdmin(admin.ModelAdmin):
    list_display = ['id', 'chapter', 'user', 'status']
    search_fields = ['user', 'chapter']
    raw_id_fields = ['user']


admin.site.register(DownLoadBook, DownloadAdmin)


class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'following_user_id']
    search_fields = []
    raw_id_fields = []


admin.site.register(UserFollowing, UserFollowingAdmin)