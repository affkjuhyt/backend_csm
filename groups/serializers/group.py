import logging

from rest_framework import serializers

from apps.vadmin.op_drf.serializers import CustomModelSerializer
from groups.models import Group, GroupUser

logger = logging.getLogger(__name__)


from datetime import datetime
today = datetime.now()
today_path = today.strftime("%Y/%m/%d")


class GroupDataSerializer(CustomModelSerializer):
    """
    GroupDataSerializer
    """

    class Meta:
        model = Group
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        group_user = GroupUser.objects.filter(group=instance)
        response['member_count'] = group_user.count()
        return response


class ExportGroupDataSerializer(CustomModelSerializer):
    """
    ExportGroupDataSerializer
    """

    class Meta:
        model = Group
        fields = ('id', 'name', 'post_count', 'member_count')

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['name_book'] = instance.book.title
    #     return response


class GroupDataCreateUpdateSerializer(CustomModelSerializer):
    """
    GroupCreateSerializer
    """

    class Meta:
        model = Group
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'post_count', 'member_count', 'date_added', 'date_modified', 'is_deleted']
        read_only_fields = ['id']

    def __str__(self):
        return "%s" % self.name
