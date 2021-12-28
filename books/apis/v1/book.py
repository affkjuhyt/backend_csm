import logging
import os
import zipfile
from io import BytesIO

from books.models.image import Image as ImageBook
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSetMixin
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from datetime import datetime

from books.serializers.book import BookAdminSerializer, BookAdminViewSerializer
from books.serializers.chapter import ChapterViewSerializer

today = datetime.now()
today_path = today.strftime("%Y/%m/%d")

from bookcase.models import History
from books.models import Book, Comment, TagBook, Tag, Chapter, Reply, HistorySearch
from books.serializers import BookSerializer, CommentSerializer, ChapterSerializer
from userprofile.models import FollowBook, DownLoadBook
from application.authentications import BaseUserJWTAuthentication

logger = logging.getLogger(__name__.split('.')[0])


class BookView(ReadOnlyModelViewSet):
    serializer_class = BookAdminSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    filter_fields = ['is_enable']

    def get_queryset(self):
        return Book.objects.filter().order_by('-date_added')

    @action(detail=False, methods=['get'], url_path='page_book')
    def get_page_book(self, request, *args, **kwargs):
        type_book = request.GET.get('type_book', '')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        if type_book == 'hot':
            books = Book.objects.order_by('-view_count', '-rate', '-like_count')
        elif type_book == 'new':
            books = Book.objects.order_by('-date_added')
        elif type_book == 'full':
            books = Book.objects.filter(is_full=True)
        elif type_book == 'propose':
            books = Book.objects.filter(is_suggest=True)
        else:
            books = Book.objects.filter()

        result_page = paginator.paginate_queryset(books, request)
        serializer = BookAdminViewSerializer(result_page, context={"request": request}, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='search')
    def search_book(self, request, *args, **kwargs):
        search_vectors = SearchVector('title', weight='A') + SearchVector('author', weight='B') \
                         + SearchVector('tagbook__tag__name', weight='C') + SearchVector('description', weight='D')

        text = request.GET.get('params', '')
        search_query = SearchQuery(text)
        search_rank = SearchRank(search_vectors, search_query)
        books = Book.objects.annotate(
            rank=search_rank
        ).order_by('-rank')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        token = request.META.get('HTTP_AUTHORIZATION', " ")
        if token == ' ':
            pass
        else:
            data = {'token': token}
            try:
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                request.user = user
            except ValidationError as v:
                print("validation error", v)
            HistorySearch.objects.create(user=self.request.user, text=text)

        result_page = paginator.paginate_queryset(books, request)
        list_books = BookSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(list_books.data)

    @action(detail=True, methods=['get'], url_path='total_comment', serializer_class=CommentSerializer)
    def get_comment(self, request, *args, **kwargs):
        book = self.get_object()

        paginator = PageNumberPagination()
        paginator.page_size = 10

        comments = Comment.objects.filter(book=book).order_by('-like_count')
        result_page = paginator.paginate_queryset(comments, request)
        list_comments = CommentSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(list_comments.data)

    @action(detail=True, methods=['get'], url_path='comment_out_standing', serializer_class=CommentSerializer)
    def get_comment_out_standing(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        book = self.get_object()
        comment = Comment.objects.filter(book=book).order_by('-like_count')
        result_page = paginator.paginate_queryset(comment, request)
        comment_out_standings = CommentSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(comment_out_standings.data)

    @action(detail=False, methods=['get'], url_path='suggest_book')
    def get_suggest_book(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 10

        # Cho nay se lam recommend system
        book = Book.objects.filter().order_by('-rate')
        result_page = paginator.paginate_queryset(book, request)
        list_suggest_books = BookSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(list_suggest_books.data)


class BookAdminView(ViewSetMixin, generics.RetrieveUpdateAPIView, generics.ListCreateAPIView):
    serializer_class = BookSerializer
    authentication_classes = [BaseUserJWTAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Book.objects.filter()

    @action(detail=False, methods=['post'], url_path='create_book', serializer_class=BookSerializer)
    def post_create_book(self, request, delete_zip_import=True, *args, **kwargs):
        zip_import = request.FILES['zip_import']
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
        return Response("Successfully")

    @action(detail=False, methods=['get'], url_path='relate_to', serializer_class=BookSerializer)
    def get_relate_to(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        user = self.request.user
        list_history = History.objects.filter(user=user)
        if len(list_history) > 0:
            for history in list_history:
                book = Book.objects.filter(id=history.book.id).first()
                tag_book_ids = TagBook.objects.filter(book_id=book.id).values_list('id', flat=True)
                tag_ids = Tag.objects.filter(tagbook__in=tag_book_ids).values_list('id', flat=True)
                tag_book_list = TagBook.objects.filter(tag__in=tag_ids).values_list('book_id', flat=True)
                books = Book.objects.filter(pk__in=tag_book_list)
                result_page = paginator.paginate_queryset(books, request)
                serializer = BookSerializer(result_page, context={"request": request}, many=True)
                return paginator.get_paginated_response(serializer.data)
        else:
            return Response("Khong co truyen lien quan")

    @action(detail=True, methods=['posts'], url_path='follow_book')
    def post_follow_book(self, request, *args, **kwargs):
        try:
            book = self.get_object()
            user = self.request.user
            follow = FollowBook.objects.filter(user=user, book=book).first()
            if follow.DoesNotExist:
                if follow.status:
                    follow.status = False
                else:
                    follow.status = True
                follow.save()
            else:
                FollowBook.objects.create(book=book, user=user)
            return Response("Create follow success", status=status.HTTP_200_OK)
        except:
            return Response("Error", status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['posts'], url_path='delete_download')
    def post(self, request, *args, **kwargs):
        try:
            book = self.get_object()
            user = self.request.user
            chapter_ids = Chapter.objects.filter(book=book).values_list('id', flat=True)
            DownLoadBook.objects.filter(chapter__in=chapter_ids).filter(user=user).update(
                status=DownLoadBook.NOT_DOWNLOAD)

            return Response("Delete download successfully", status=status.HTTP_200_OK)
        except:
            return Response("Error", status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='list_chapter_download')
    def get_list_chapter_download(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        user = self.request.user
        book = self.get_object()
        chapters = Chapter.objects.filter(book=book)

        result_page = paginator.paginate_queryset(chapters, request)
        serializer = ChapterViewSerializer(result_page, context={"request": request}, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True, methods=['posts'], url_path='add_comment')
    def post_add_comment(self, request, *args, **kwargs):
        content = request.data['content']
        comment_id = request.data['comment_id']
        try:
            user = self.request.user
            book = self.get_object()
            if comment_id == "":
                Reply.objects.create(comment_id=comment_id, user=user, content=content)
            else:
                Comment.objects.create(user=user, book=book, content=content)
            return Response("Create comment successfully", status=status.HTTP_200_OK)
        except:
            return Response("Error", status=status.HTTP_404_NOT_FOUND)
