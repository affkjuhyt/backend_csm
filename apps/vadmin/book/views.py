import os
import zipfile
from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

from apps.vadmin.book.filter import BookDataFilter, ChapterDataFilter, SaveImageFilter, CommentFilter
from apps.vadmin.book.models import Book, Chapter, Comment
from apps.vadmin.book.serializers.book import BookDataSerializer, BookDataCreateUpdateSerializer, \
    ExportBookDataSerializer
from apps.vadmin.book.models.image import Image as ImageBook, Image
from apps.vadmin.book.serializers.chapter import ChapterDataSerializer, ChapterDataCreateUpdateSerializer, \
    ExportChapterDataSerializer, today_path
from apps.vadmin.book.serializers.comment import CommentDataSerializer
from apps.vadmin.book.serializers.image import SaveImageSerializer, SaveImageCreateUpdateSerializer, ImageDataSerializer
from apps.vadmin.op_drf.response import SuccessResponse
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.permission.permissions import CommonPermission, User
from apps.vadmin.utils.export_excel import export_excel_save_model
from apps.vadmin.utils.file_util import get_all_files, delete_files, remove_empty_dir


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
        paginator.page_query_param = 'pageNum'
        book_id = int(request.GET.get('book'))
        title = request.GET.get('title')
        if not title:
            paginator.page_size = 3000
            title = ""
        if not book_id:
            book_id = ""
        chapters = Chapter.objects.filter(book_id=book_id, title__contains=title).order_by('-id')
        result_page = paginator.paginate_queryset(chapters, request)
        list_chapters = ChapterDataSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(list_chapters.data)


class ChapterAdminViewSet(ViewSetMixin, generics.RetrieveUpdateAPIView, generics.ListCreateAPIView):
    serializer_class = ChapterDataSerializer
    filter_class = ChapterDataFilter
    search_fields = ('title',)
    ordering = 'number'

    def get_queryset(self):
        return Chapter.objects.filter()

    def update_chapter(self, request, *args, **kwargs):
        zip_import = request.data.get('file')
        data = request.data
        title = data.get('title')
        number = int(data.get('number'))
        description = data.get('description')
        chapter = Chapter.objects.filter(number=number).first()
        # book = Chapter.objects.filter(title=title, number=number, description=description)
        # Get ra name thu muc de luu vao chuong
        # Sau do lay image de luu vao chuong
        zip_file = zipfile.ZipFile(zip_import)
        for name in zip_file.namelist():
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
            ImageBook.objects.create(image=saved_path, chapter=chapter)
        return Response("Successfully create chapter")


class ImageDataModelViewSet(CustomModelViewSet):
    queryset = Image.objects.all()
    serializer_class = SaveImageSerializer
    create_serializer_class = SaveImageCreateUpdateSerializer
    update_serializer_class = SaveImageCreateUpdateSerializer
    filter_class = SaveImageFilter
    # extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    search_fields = ('configName',)
    ordering = '-create_datetime'

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return SuccessResponse(serializer.data, status=201, headers=headers)

    def clearimagefile(self, request: Request, *args, **kwargs):
        file_list = get_all_files(os.path.join(settings.MEDIA_ROOT, 'system'))
        queryset_files = [os.path.join(os.path.join(settings.MEDIA_ROOT) + os.sep, ele) for ele in
                          list(self.get_queryset().values_list('file', flat=True))]
        queryset_files_dir = set(map(lambda absdir: os.path.abspath(absdir), queryset_files))
        delete_list = list(set(file_list) - queryset_files_dir)
        delete_files(delete_list)
        remove_empty_dir(os.path.join(settings.MEDIA_ROOT, 'system'))
        return SuccessResponse(msg=f"Dọn dẹp thành công {len(delete_list)} các tệp lỗi thời")

    @action(detail=False, methods=['get'], url_path='filter', filter_class=SaveImageFilter)
    def get_book(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginator.page_query_param = 'pageNum'
        book_id = request.GET.get('book')
        creator_name = request.GET.get('creator_name')
        chapter_ids = request.GET.get('chapter')
        if not book_id and not creator_name and not chapter_ids:
            chapter_ids = Chapter.objects.filter().values_list('id')
        else:
            if not chapter_ids:
                chapter_ids = Chapter.objects.filter(book_id=book_id).values_list('id')
            else:
                chapter_ids = Chapter.objects.filter(book_id=book_id, id=chapter_ids).values_list('id')
        images = Image.objects.filter(chapter__in=chapter_ids).order_by('-id')
        result_page = paginator.paginate_queryset(images, request)
        list_images = SaveImageSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(list_images.data)


class CommentAdminViewSet(ViewSetMixin, generics.RetrieveUpdateAPIView, generics.ListCreateAPIView):
    serializer_class = CommentDataSerializer
    filter_class = CommentFilter
    search_fields = ('chapter', 'book',)
    ordering = '-like_count'

    def get_queryset(self):
        return Comment.objects.filter()
