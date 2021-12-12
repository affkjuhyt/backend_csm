import logging

from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSetMixin
from rest_framework.filters import SearchFilter

from books.models import Book
from books.serializers import BookSerializer
from application.authentications import BaseUserJWTAuthentication
from userprofile.models import FollowBook
from userprofile.serializers import FollowBookSerializer


class FollowBookAdminView(ViewSetMixin, generics.RetrieveUpdateAPIView, generics.ListCreateAPIView):
    serializer_class = FollowBookSerializer
    authentication_classes = [BaseUserJWTAuthentication]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return FollowBook.objects.filter()

    @action(detail=False, methods=['get'], url_path='book_follow')
    def get_book_follow(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        user = self.request.user
        book_ids = FollowBook.objects.filter(user=user).values_list('book_id', flat=True)
        books = Book.objects.filter(pk__in=book_ids)
        result_page = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(serializer.data)
