from requests import Response
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSetMixin

from apps.vadmin.op_drf.response import SuccessResponse
from books.models import Book, Comment
from books.serializers import BookSerializer
from application.authentications import BaseUserJWTAuthentication
from posts.models import PostGroup
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

    @action(detail=False, methods=['post'], url_path='like')
    def post_like(self, request, *args, **kwargs):
        type_like = request.data.get("type_like")
        if type_like == 'book':
            book_id = request.data.get("book")
            book = Book.objects.filter(pk=book_id).first()
            book.like_count = book.like_count + 1
            book.save()

            return SuccessResponse("Like book successfully", status=status.HTTP_200_OK)
        elif type_like == 'comment':
            comment_id = request.data.get('comment')
            comment = Comment.objects.filter(pk=comment_id).first()
            comment.like_count = comment.like_count + 1
            comment.save()

            return SuccessResponse("Like comment successfully", status=status.HTTP_200_OK)
        else:
            post_id = request.data.get('post')
            post = PostGroup.objects.filter(pk=post_id).first()
            post.like_count = post.like_count + 1
            post.save()

            return SuccessResponse("Like post successfully", status=status.HTTP_200_OK)
