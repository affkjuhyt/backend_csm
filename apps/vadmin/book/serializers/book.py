from apps.vadmin.book.models import Book
from apps.vadmin.op_drf.serializers import CustomModelSerializer


class BookDataSerializer(CustomModelSerializer):
    """
    BookDataSerializer
    """

    class Meta:
        model = Book
        exclude = ('creator', 'modifier')


class ExportBookDataSerializer(CustomModelSerializer):
    """
    ExportBookDataSerializer
    """

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'status', 'type', 'like_count', 'view_count', 'star', 'description')


class BookDataCreateUpdateSerializer(CustomModelSerializer):
    """
    BookCreateSerializer
    """

    class Meta:
        model = Book
        fields = '__all__'

