import logging

from rest_framework import serializers

from groups.models import GroupUser

logger = logging.getLogger(__name__)


class GroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupUser
        fields = ['id', 'group', 'user', 'date_added', 'date_modified', 'is_deleted']
        read_only_fields = ['id']

    def __str__(self):
        return "%s" % self.id
