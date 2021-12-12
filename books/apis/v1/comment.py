import logging

from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSetMixin

from books.models import Comment
from books.serializers import CommentSerializer
from application.authentications import BaseUserJWTAuthentication
from books.serializers.comment import CreateCommentDataSerializer

logger = logging.getLogger(__name__.split('.')[0])


class CommentView(ReadOnlyModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    search_fields = ['content']

    def get_queryset(self):
        return Comment.objects.filter().order_by('-like_count')


class CommentPostView(ViewSetMixin, generics.RetrieveUpdateAPIView, generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    authentication_classes = [BaseUserJWTAuthentication]
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


    def get_queryset(self):
        return Comment.objects.filter()

    @action(detail=False, methods=['post'], url_path='post_comment')
    def post(self, request):
        # serializer = CreateCommentDataSerializer(data=request.data)
        book = request.data['book']
        if request.data['chapter'] == "":
            chapter = ""
        else:
            chapter = request.data['chapter']
        user = request.data['user']
        content = request.data['content']
        try:
            comment = Comment.objects.create(book_id=book, chapter_id=chapter, user_id=user, content=content)
            comment.save()
            return Response("Create book successfully", status=status.HTTP_200_OK)
        except:
            return Response("Create book false", status=status.HTTP_404_NOT_FOUND)
