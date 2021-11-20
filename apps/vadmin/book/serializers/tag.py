from apps.vadmin.book.models import Tag, TagBook
from apps.vadmin.op_drf.serializers import CustomModelSerializer

from datetime import datetime
today = datetime.now()
today_path = today.strftime("%Y/%m/%d")


class TagDataSerializer(CustomModelSerializer):
    """
    TagDataSerializer
    """

    class Meta:
        model = Tag
        fields = '__all__'

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['name_book'] = instance.book.title
    #     return response


class ExportTagDataSerializer(CustomModelSerializer):
    """
    ExportTagDataSerializer
    """

    class Meta:
        model = Tag
        fields = ('id', 'name', 'update_datetime', 'create_datetime')

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['name_book'] = instance.book.title
    #     return response


class TagDataCreateUpdateSerializer(CustomModelSerializer):
    """
    TagCreateSerializer
    """

    class Meta:
        model = Tag
        fields = '__all__'

