import logging

from rest_framework import serializers

from apps.vadmin.userprofile.models.follow_book import FollowBook

logger = logging.getLogger(__name__.split('.')[0])


class FollowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowBook
        fields = ['id', 'user', 'book', 'status']
        read_only_fields = ['id']
