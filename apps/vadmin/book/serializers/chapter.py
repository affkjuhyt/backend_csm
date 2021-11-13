from apps.vadmin.book.models import Chapter
from apps.vadmin.op_drf.serializers import CustomModelSerializer


class ChapterDataSerializer(CustomModelSerializer):
    """
    ChapterDataSerializer
    """

    class Meta:
        model = Chapter
        exclude = ('creator', 'modifier')


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

