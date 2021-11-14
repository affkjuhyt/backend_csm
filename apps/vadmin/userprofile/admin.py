from django.contrib import admin

from apps.vadmin.userprofile.models import Profile, FollowBook, UserFollowing


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'full_name', 'user_type', 'coin']
    search_fields = ['full_name', 'email']
    raw_id_fields = []


admin.site.register(Profile, ProfileAdmin)


class FollowBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'status']
    search_fields = ['user', 'book']
    raw_id_fields = ['user']


admin.site.register(FollowBook, FollowBookAdmin)


class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'following_user_id']
    search_fields = []
    raw_id_fields = []


admin.site.register(UserFollowing, UserFollowingAdmin)