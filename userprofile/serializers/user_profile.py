import logging

from rest_framework import serializers

from apps.vadmin.permission.models.users import UserProfile

logger = logging.getLogger(__name__.split('.')[0])


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'full_name', 'phone_number', 'email', 'gender',
                  'user_type', 'level', 'coin', 'point', 'avatar']
        read_only_fields = ['id']
