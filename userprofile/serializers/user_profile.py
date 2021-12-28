import logging

from rest_framework import serializers

from apps.vadmin.permission.models.users import UserProfile
from posts.models import PostGroup
from posts.serializers import PostGroupSerializer
from userprofile.models import UserFollowing

logger = logging.getLogger(__name__.split('.')[0])


class UserProfileSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'full_name', 'phone_number', 'email', 'gender',
                  'user_type', 'level', 'coin', 'point', 'avatar', 'post']
        read_only_fields = ['id']

    def to_representation(self, instance):
        user = self.context.get('request').user
        response = super().to_representation(instance)
        response['count_following'] = instance.following.all().count()
        response['count_follower'] = instance.followers.all().count()
        u_following = UserFollowing.objects.filter(user_id=user, following_user_id=instance)
        response['status_following'] = True
        if len(u_following) == 0:
            response['status_following'] = False

        return response

    def get_post(self, obj):
        post_group = PostGroup.objects.filter(user_id=obj.id)

        return PostGroupSerializer(post_group, many=True).data


class UserProfilePublicSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'full_name', 'phone_number', 'email', 'gender',
                  'user_type', 'level', 'coin', 'point', 'avatar', 'post']
        read_only_fields = ['id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['count_following'] = instance.following.all().count()
        response['count_follower'] = instance.followers.all().count()
        response['status_following'] = False

        return response

    def get_post(self, obj):
        post_group = PostGroup.objects.filter(user_id=obj.id)

        return PostGroupSerializer(post_group, many=True).data


