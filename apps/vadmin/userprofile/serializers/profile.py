import logging

from rest_framework import serializers

# from userprofile.models import UserProfile
from apps.vadmin.userprofile.models.profile import Profile

logger = logging.getLogger(__name__.split('.')[0])


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'phone_number', 'email', 'gender',
                  'user_type', 'level', 'coin', 'point', 'avatar']
        read_only_fields = ['id']
