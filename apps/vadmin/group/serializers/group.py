from apps.vadmin.group.models import Group, GroupUser
from apps.vadmin.op_drf.serializers import CustomModelSerializer

from datetime import datetime
today = datetime.now()
today_path = today.strftime("%Y/%m/%d")


class GroupDataSerializer(CustomModelSerializer):
    """
    GroupDataSerializer
    """

    class Meta:
        model = Group
        exclude = ('creator', 'modifier')

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
        fields = ('id', 'name', 'post_count', 'member_count', 'description')

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

