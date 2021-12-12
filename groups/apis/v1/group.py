import logging

from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin, ReadOnlyModelViewSet

from groups.models import Group
from groups.serializers import GroupSerializer
from posts.models import PostGroup
from posts.serializers import PostGroupSerializer

logger = logging.getLogger(__name__.split('.')[0])


class GroupView(ReadOnlyModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filter_backends = [SearchFilter]

    def get_queryset(self):
        return Group.objects.filter()

    @action(detail=True, methods=['get'], url_path='post_group')
    def get_post_group(self, request, *args, **kwargs):
        group = self.get_object()
        posts = PostGroup.objects.filter(group=group)
        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(posts, request)
        list_comments = PostGroupSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(list_comments.data)

