import logging
import os
import zipfile
from io import StringIO, BytesIO
from zipfile import ZipFile

from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# import root.settings
from books.serializers.chapter import ChapterAdminSerializer
# from root import settings
from application.authentications import BaseUserJWTAuthentication
from books.models import Book, Chapter, Comment, Image
from userprofile.models import DownLoadBook
from books.serializers import BookSerializer, ChapterSerializer, ImageSerializer
from bookcase.models import History
from rest_framework.viewsets import ViewSetMixin, ReadOnlyModelViewSet

logger = logging.getLogger(__name__.split('.')[0])


# def modify_input_for_multiple_files(chapter_id, image):
#     dict = {}
#     dict['chapter'] = chapter_id
#     dict['image'] = image
#     return dict


class ChapterAdminView(ViewSetMixin, generics.RetrieveUpdateAPIView, generics.ListCreateAPIView):
    serializer_class = ChapterAdminSerializer

    # authentication_classes = [BaseUserJWTAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Chapter.objects.filter()

    @action(detail=True, methods=['get'], url_path='download', serializer_class=ChapterSerializer)
    def get_download(self, request, *args, **kwargs):
        chapter = self.get_object()
        images = Image.objects.filter(chapter=chapter)
        filelist = []
        for image in images:
            filelist.append(image.image.url)

        # filelist = [MyModel.path_to_file1, MyModel.path_to_file2, MyModel.path_to_file3]
        byte_data = BytesIO()
        zip_name = "%s.zip" % chapter.id
        zip_file = zipfile.ZipFile(byte_data, 'w')

        for file in filelist:
            filename = os.path.basename(os.path.normpath(file))
            zip_file.write(file, filename)
        zip_file.close()

        response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=%s' % zip_name

        zip_file.printdir()

        return response

    @action(detail=True, methods=['posts'], url_path='action_chapter', serializer_class=ChapterSerializer)
    def post_action_chapter(self, request, *args, **kwargs):
        user = self.request.user
        chapter = self.get_object()
        book = Book.objects.filter(chapter=chapter).first()

        history = History.objects.filter(user=user, book=book).first()
        if history.DoesNotExist:
            if history.chapter_id > chapter.number:
                pass
            else:
                history.chapter = chapter
                history.save()
        else:
            History.objects.create(user=user, book=book, chapter=chapter)

        return Response('Write log success', status=status.HTTP_200_OK)

    @action(detail=True, methods=['posts'], url_path='delete_download')
    def post_delete_download(self, request, *args, **kwargs):
        chapter = self.get_object()
        download_book = DownLoadBook.objects.filter(chapter=chapter).filter(user=self.request.user)
        if len(download_book) > 0:
            download_book.update(status=DownLoadBook.NOT_DOWNLOAD)

            return Response("Delete book downloaded successfully", status=status.HTTP_200_OK)
        else:
            return Response("Khong co chapter nay", status=status.HTTP_404_NOT_FOUND)

    # @action(detail=True, methods=['posts'], url_path='create_book')
    # def post_book(self, request, *args, **kwargs):
    #     chapter_id = self.get_object().id
    #     images = dict((request.data).lists())['image']
    #     flag = 1
    #     arr = []
    #     for img_name in images:
    #         modified_data = modify_input_for_multiple_files(chapter_id,
    #                                                         img_name)
    #         file_serializer = ImageSerializer(data=modified_data)
    #         if file_serializer.is_valid():
    #             file_serializer.save()
    #             arr.append(file_serializer.data)
    #         else:
    #             flag = 0
    #     if flag == 1:
    #         return Response(arr, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(arr, status=status.HTTP_400_BAD_REQUEST)


class ChapterView(ReadOnlyModelViewSet):
    serializer_class = ChapterAdminSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filter_backends = [SearchFilter]

    def get_queryset(self):
        return Chapter.objects.filter()

    @action(detail=True, methods=['get'], url_path='view_book')
    def get_view_book(self, request, *args, **kwargs):
        chapter = self.get_object()
        image = Image.objects.filter(chapter=chapter)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(image, request)
        serializer = ImageSerializer(result_page, context={"request": request}, many=True)
        return paginator.get_paginated_response(serializer.data)
