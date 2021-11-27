from apps.vadmin.post.models import PostGroup
from apps.vadmin.op_drf.serializers import CustomModelSerializer

from datetime import datetime
today = datetime.now()
today_path = today.strftime("%Y/%m/%d")


class PostGroupDataSerializer(CustomModelSerializer):
    """
    PostGroupDataSerializer
    """

    class Meta:
        model = PostGroup
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = instance.user.name
        response['group'] = instance.group.name
        return response


class ExportPostGroupDataSerializer(CustomModelSerializer):
    """
    ExportPostGroupDataSerializer
    """

    class Meta:
        model = PostGroup
        fields = '__all__'

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['name_book'] = instance.book.title
    #     return response


class PostGroupDataCreateUpdateSerializer(CustomModelSerializer):
    """
    PostGroupCreateSerializer
    """

    class Meta:
        model = PostGroup
        fields = '__all__'

