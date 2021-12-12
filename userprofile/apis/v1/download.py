import logging

from functools import reduce
from operator import or_

from django.db.models import Q
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

from books.models import Book, Chapter
from books.serializers import BookSerializer
from application.authentications import BaseUserJWTAuthentication
from userprofile.models import DownLoadBook
from userprofile.serializers import DownloadBookSerializer


class DownloadBookAdminView(ViewSetMixin, generics.RetrieveUpdateAPIView, generics.ListCreateAPIView):
    serializer_class = DownloadBookSerializer
    authentication_classes = [BaseUserJWTAuthentication]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return DownLoadBook.objects.filter()

    @action(detail=False, methods=['get'], url_path='list_download')
    def get_book_follow(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        user = self.request.user
        download_lists = DownLoadBook.objects.filter(user=user).exclude(
            status=[DownLoadBook.NOT_DOWNLOAD, DownLoadBook.ERROR]).values_list('chapter_id', flat=True)
        books = Book.objects.filter(chapter__in=download_lists).distinct()
        result_page = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(serializer.data)
