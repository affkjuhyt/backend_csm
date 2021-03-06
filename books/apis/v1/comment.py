import logging
import re

from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSetMixin
from django.db.models import Q, CharField
from django.db.models.functions import Lower


from books.models import Comment, Reply, VulgarWord
from books.serializers import CommentSerializer
from application.authentications import BaseUserJWTAuthentication
from books.serializers.comment import ReplySerializer

logger = logging.getLogger(__name__.split('.')[0])

CharField.register_lookup(Lower, "lower")


class CommentView(ReadOnlyModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    search_fields = ['content']

    def get_queryset(self):
        return Comment.objects.filter().order_by('-like_count')

    @action(detail=True, methods=['get'], url_path='reply')
    def get_reply(self, request, *args, **kwargs):
        comment = self.get_object()
        # first = Reply.objects.filter().first()
        replys = Reply.objects.filter(comment=comment)[1:]

        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(replys, request)
        list_comments = ReplySerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(list_comments.data)


class CommentPostView(ViewSetMixin, generics.RetrieveUpdateAPIView, generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    authentication_classes = [BaseUserJWTAuthentication]
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return Comment.objects.filter()

    @action(detail=False, methods=['post'], url_path='post_comment')
    def post(self, request, *args, **kwargs):
        # serializer = CreateCommentDataSerializer(data=request.data)
        if request.data['book'] == "":
            book = ""
        else:
            book = request.data['book']
        if request.data['post'] == "":
            post = ""
        else:
            post = request.data['post']
        if request.data['chapter'] == "":
            chapter = ""
        else:
            chapter = request.data['chapter']
        user = request.user
        content = request.data['content']
        try:
            new_list = []
            content_slices = re.findall(r'\S+', content)
            for content_slice in content_slices:
                vulgar = VulgarWord.objects.filter(Q(word__lower__contains=content_slice.lower()))
                if len(vulgar) > 0:
                    re_word = vulgar.get().re_word
                    new_list.append(re_word)
                else:
                    new_list.append(content_slice)

            list_to_str = ' '.join(map(str, new_list))
            comment = Comment.objects.create(book_id=book, chapter_id=chapter, user=user, content=list_to_str,
                                             post_id=post)
            comment.save()

            return Response("Create comment successfully", status=status.HTTP_200_OK)
        except:
            return Response("Create comment false", status=status.HTTP_404_NOT_FOUND)
