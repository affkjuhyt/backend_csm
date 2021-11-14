import os
import zipfile
from io import BytesIO

from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

from apps.vadmin.book.filter import BookDataFilter, ChapterDataFilter
from apps.vadmin.book.models import Book, Chapter
from apps.vadmin.book.serializers.book import BookDataSerializer, BookDataCreateUpdateSerializer, \
    ExportBookDataSerializer
from apps.vadmin.book.models.image import Image as ImageBook
from apps.vadmin.book.serializers.chapter import ChapterDataSerializer, ChapterDataCreateUpdateSerializer, \
    ExportChapterDataSerializer, today_path
from apps.vadmin.op_drf.filters import DataLevelPermissionsFilter
from apps.vadmin.op_drf.response import SuccessResponse
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.permission.permissions import CommonPermission
from apps.vadmin.utils.export_excel import export_excel_save_model


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
    # create_serializer_class = ChapterDataCreateUpdateSerializer
    # update_serializer_class = ChapterDataCreateUpdateSerializer
    filter_class = ChapterDataFilter
    # update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    # create_extra_permission_classes = (CommonPermission,)
    search_fields = ('title',)
    ordering = 'number'

    def export(self, request: Request, *args, **kwargs):
        """
        Export data chapter
        """

        book_id = int(request.query_params.get('book'))
        field_data = ['STT', 'Tên chương', 'BookId', 'Number', 'Thubmnail', 'Like', 'Tên truyện']
        data = ExportChapterDataSerializer(Chapter.objects.filter(book_id=book_id), many=True).data
        return SuccessResponse(export_excel_save_model(request, field_data, data, f'导出字典[{book_id}]详情数据.xls'))

    @action(detail=False, methods=['get'], url_path='book_chapter', filter_class=ChapterDataFilter)
    def get_book(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        book_id = int(request.GET.get('book'))
        title = request.GET.get('title')
        chapters = Chapter.objects.filter(book_id=book_id, title__contains=title)
        result_page = paginator.paginate_queryset(chapters, request)
        list_chapters = ChapterDataSerializer(result_page, many=True)

        return paginator.get_paginated_response(list_chapters.data)


class ChapterAdminViewSet(ViewSetMixin, generics.RetrieveUpdateAPIView, generics.ListCreateAPIView):
    serializer_class = ChapterDataSerializer
    filter_class = ChapterDataFilter
    search_fields = ('title',)
    ordering = 'number'

    def get_queryset(self):
        return Chapter.objects.filter()

    def update_chapter(self, request, *args, **kwargs):
        breakpoint()
        zip_import = request.FILES['file']
        data = request.data
        name = data.get('name')
        author = data.get('author')
        description = data.get('description')

        book = Book.objects.create(title=name, author=author, description=description)
        # Get ra name thu muc de luu vao chuong
        # Sau do lay image de luu vao chuong
        zip_file = zipfile.ZipFile(zip_import)
        chapter = []
        for name in zip_file.namelist():
            if ".png" not in name:
                name = name[:-1]
                chapter.append(name)
                Chapter.objects.create(title=name, book_id=book.id)
            else:
                data = zip_file.read(name)
                try:
                    from PIL import Image
                    image = Image.open(BytesIO(data))
                    image.load()
                    image = Image.open(BytesIO(data))
                    image.verify()
                except ImportError:
                    pass
                except:
                    continue
                name = os.path.split(name)[1]
                path = os.path.join('books', today_path, name)
                saved_path = default_storage.save(path, ContentFile(data))
                chapter_last = Chapter.objects.filter().last()
                ImageBook.objects.create(image=saved_path, chapter=chapter_last)
        return Response("Successfully create chapter")

