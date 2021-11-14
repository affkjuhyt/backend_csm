from django.conf import settings
from django.core.cache import cache
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from apps.vadmin.book.filter import BookDataFilter, ChapterDataFilter
from apps.vadmin.book.models import Book, Chapter
from apps.vadmin.book.serializers.book import BookDataSerializer, BookDataCreateUpdateSerializer, \
    ExportBookDataSerializer
from apps.vadmin.book.serializers.chapter import ChapterDataSerializer, ChapterDataCreateUpdateSerializer
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


class ChapterDataModelViewSet(CustomModelViewSet):
    """
    CRUD
    """
    queryset = Chapter.objects.all()
    serializer_class = ChapterDataSerializer
    create_serializer_class = ChapterDataCreateUpdateSerializer
    update_serializer_class = ChapterDataCreateUpdateSerializer
    filter_class = ChapterDataFilter
    export_field_data = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    search_fields = ('title',)
    ordering = 'number'

    @action(detail=False, methods=['get'], url_path='book_chapter')
    def get_book(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        book_id = int(request.GET.get('book'))
        chapters = Chapter.objects.filter(book_id=book_id)
        result_page = paginator.paginate_queryset(chapters, request)
        list_chapters = ChapterDataSerializer(result_page, many=True)

        return paginator.get_paginated_response(list_chapters.data)
