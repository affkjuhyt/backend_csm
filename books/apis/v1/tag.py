import logging

from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.vadmin.op_drf.response import SuccessResponse
from books.models import Tag, TagBook, Book
from books.serializers.book import BookAdminViewSerializer
from books.serializers.tag import TagPublicViewSerializer

logger = logging.getLogger(__name__.split('.')[0])


class TagView(ReadOnlyModelViewSet):
    serializer_class = TagPublicViewSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        return Tag.objects.filter()

    @action(detail=True, methods=['get'], url_path='book')
    def get_tag_book(self, request, *args, **kwargs):
        tag_book_ids = TagBook.objects.filter(tag__name=self.get_object().name).values_list('book')
        books = Book.objects.filter(pk__in=tag_book_ids)[:50]
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(books, request)
        list_books = BookAdminViewSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(list_books.data)

