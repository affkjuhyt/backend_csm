from django.conf import settings
from django.core.cache import cache
from rest_framework.request import Request

from apps.vadmin.book.filter import BookDataFilter
from apps.vadmin.book.models import Book, Chapter
from apps.vadmin.book.serializers.book import BookDataSerializer, BookDataCreateUpdateSerializer, \
    ExportBookDataSerializer
from apps.vadmin.book.serializers.chapter import ChapterDataSerializer
from apps.vadmin.op_drf.filters import DataLevelPermissionsFilter
from apps.vadmin.op_drf.response import SuccessResponse
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.permission.permissions import CommonPermission


class BookDataModelViewSet(CustomModelViewSet):
    """
    CRUD
    """
    queryset = Book.objects.all()
    serializer_class = BookDataSerializer
    create_serializer_class = BookDataCreateUpdateSerializer
    update_serializer_class = BookDataCreateUpdateSerializer
    # extra_filter_backends = [DataLevelPermissionsFilter]
    filter_class = BookDataFilter
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    search_fields = ('title', 'type')
    ordering = 'id'
    export_field_data = ['ID', 'Tên', 'Tác giả', 'Trạng thái', 'Thể loại', 'Star', 'View', 'Like', 'Miêu tả']
    export_serializer_class = ExportBookDataSerializer


# class ChapterDataModelViewSet(CustomModelViewSet):
#     """
#     CRUD
#     """
#     queryset = Chapter.objects.all()
#     serializer_class = ChapterDataSerializer
#     create_serializer_class =
