import logging

from rest_framework import serializers

from userprofile.models import FollowBook

logger = logging.getLogger(__name__.split('.')[0])


class FollowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowBook
        fields = ['id', 'user', 'book', 'status']
        read_only_fields = ['id']
