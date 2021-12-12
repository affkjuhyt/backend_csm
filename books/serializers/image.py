import logging

from rest_framework import serializers

from apps.vadmin.op_drf.serializers import CustomModelSerializer
from books.models import Image

logger = logging.getLogger(__name__)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'chapter', 'image', 'date_modified', 'date_added', 'is_deleted']
        read_only_fields = ['id']


class ImageDataSerializer(CustomModelSerializer):
    """
    ImageDataSerializer
    """

    class Meta:
        model = Image
        fields = '__all__'


class ImageDataCreateUpdateSerializer(CustomModelSerializer):
    """
    ImageCreateSerializer
    """

    class Meta:
        model = Image
        fields = '__all__'


class SaveImageSerializer(CustomModelSerializer):
    # image_url = serializers.CharField(source='file.url', read_only=True)

    class Meta:
        model = Image
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['name_chapter'] = instance.chapter.title
        response['name_book'] = instance.chapter.book.title

        return response


class SaveImageCreateUpdateSerializer(CustomModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    def get_image_url(self, obj: Image):
        return getattr(obj.file, "url", obj.file) if hasattr(obj, "file") else ""

    def save(self, **kwargs):
        files = self.context.get('request').FILES.get('file')
        self.validated_data['name'] = files.name
        self.validated_data['size'] = files.size
        self.validated_data['type'] = files.content_type
        self.validated_data['address'] = 'Address'
        self.validated_data['source'] = 'Source'
        instance = super().save(**kwargs)
        return instance

    class Meta:
        model = Image
        fields = '__all__'


