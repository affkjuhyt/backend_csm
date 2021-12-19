import logging

from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin, ReadOnlyModelViewSet

from books.models import Comment
from books.serializers import CommentSerializer
from books.serializers.comment import CommentDataShowSerializer
from posts.models import PostGroup
from posts.serializers import PostGroupSerializer
from application.authentications import BaseUserJWTAuthentication

logger = logging.getLogger(__name__.split('.')[0])


class PostView(ReadOnlyModelViewSet):
    serializer_class = PostGroupSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filter_backends = [SearchFilter]

    def get_queryset(self):
        return PostGroup.objects.filter()

    @action(detail=False, methods=['get'], url_path='post_trending')
    def get_post_trending(self, request, *args, **kwargs):
        posts = PostGroup.objects.order_by('-like_count', 'share_count')
        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(posts, request)
        list_comments = PostGroupSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(list_comments.data)

    @action(detail=True, methods=['get'], url_path='comments')
    def get_comments(self, request, *args, **kwargs):
        post = self.get_object()
        comments = Comment.objects.filter(post=post)

        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(comments, request)
        list_comments = CommentDataShowSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(list_comments.data)


class PostAdminView(ViewSetMixin, generics.RetrieveUpdateAPIView, generics.ListCreateAPIView):
    serializer_class = PostGroupSerializer
    authentication_classes = [BaseUserJWTAuthentication]
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filter_backends = [SearchFilter]

    def get_queryset(self):
        return PostGroup.objects.filter()

    @action(detail=False, methods=['get'], url_path='post_user')
    def get_post_user(self, request, *args, **kwargs):
        user = self.request.user
        posts = PostGroup.objects.filter(user=user)
        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(posts, request)
        list_comments = PostGroupSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(list_comments.data)

    @action(detail=False, methods=['post'], url_path='create_post')
    def post_posts(self, request, *args, **kwargs):
        user = self.request.user
        group = request.data["group"]
        content = request.data["content"]
        image_url = request.data["image_url"]

        try:
            post_group = PostGroup.objects.create(user=user, group_id=group, content=content, image_url=image_url)
            post_group.save()

            return Response("Create post successfully", status=status.HTTP_200_OK)
        except:
            return Response("Create post failed", status=status.HTTP_404_NOT_FOUND)

