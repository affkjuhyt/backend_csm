from apps.vadmin.book.models import Chapter
from apps.vadmin.op_drf.serializers import CustomModelSerializer


class ChapterDataSerializer(CustomModelSerializer):
    """
    ChapterDataSerializer
    """

    class Meta:
        model = Chapter
        exclude = ('creator', 'modifier')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['name_book'] = instance.book.title
        return response


class ExportChapterDataSerializer(CustomModelSerializer):
    """
    ExportChapterDataSerializer
    """

    class Meta:
        model = Chapter
        fields = ('id', 'title', 'book', 'number', 'thumbnail', 'like_count')


class ChapterDataCreateUpdateSerializer(CustomModelSerializer):
    """
    ChapterCreateSerializer
    """

    class Meta:
        model = Chapter
        fields = '__all__'

