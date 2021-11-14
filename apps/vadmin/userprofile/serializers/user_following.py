import logging

from rest_framework import serializers

from django.contrib.auth import get_user_model
from apps.vadmin.userprofile.models.user_following import UserFollowing

logger = logging.getLogger(__name__.split('.')[0])

User = get_user_model()


class FollowingSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowing
        fields = ("id", "fullname", "following_user_id", "date_added", "date_modified", "is_deleted")

    def get_fullname(self, obj):
        return User.objects.filter(id=obj.following_user_id.id).first().first_name


class FollowersSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowing
        fields = ("id", "fullname", "user_id", "date_added", "date_modified", "is_deleted")

    def get_fullname(self, obj):
        return User.objects.filter(id=obj.user_id.id).first().first_name


class UserFollowingSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "following",
            "followers",
        )

    def get_following(self, obj):
        queryset = UserFollowing.objects.none()
        queryset |= UserFollowing.objects.filter(pk=obj.following_user_id.pk)
        return FollowingSerializer(queryset, many=True).data

    def get_followers(self, obj):
        queryset = UserFollowing.objects.none()
        queryset |= UserFollowing.objects.filter(pk=obj.user_id.pk)
        return FollowersSerializer(queryset, many=True).data
