from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin, ReadOnlyModelViewSet

from analytics.views import user
from application.authentications import BaseUserJWTAuthentication
from apps.vadmin.op_drf.response import SuccessResponse
from groups.models import GroupUser, Group
from groups.serializers import GroupUserSerializer, GroupSerializer


class UserGroupViewSet(ReadOnlyModelViewSet):
    serializer_class = GroupSerializer
    authentication_classes = [BaseUserJWTAuthentication]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        return Group.objects.filter()

    @action(detail=False, methods=['get'], url_path='user_group')
    def get_user_group(self, request, *args, **kwargs):
        user = self.request.user
        group_ids = GroupUser.objects.filter(user=user).values_list('group_id')
        groups = Group.objects.filter(pk__in=group_ids)
        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(groups, request)
        list_comments = GroupSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(list_comments.data)

    @action(detail=False, methods=['get'], url_path='recommender')
    def get_recommender(self, request, *args, **kwargs):
        user = self.request.user
        group_ids = GroupUser.objects.filter(user=user).values_list('group_id')
        groups = Group.objects.exclude(pk__in=group_ids)
        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(groups, request)
        list_comments = GroupSerializer(result_page, context={"request": request}, many=True)

        return paginator.get_paginated_response(list_comments.data)
