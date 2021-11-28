from django.shortcuts import render

# Create your views here.
from apps.vadmin.post.filter import PostGroupDataFilter
from apps.vadmin.post.models import PostGroup
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.permission.permissions import CommonPermission

# from rest_framework.request import Request
from apps.vadmin.post.serializers.post import PostGroupDataSerializer, PostGroupDataCreateUpdateSerializer, \
    ExportPostGroupDataSerializer


class PostGroupDataModelViewSet(CustomModelViewSet):
    queryset = PostGroup.objects.all()
    serializer_class = PostGroupDataSerializer
    create_serializer_class = PostGroupDataCreateUpdateSerializer
    update_serializer_class = PostGroupDataCreateUpdateSerializer
    filter_class = PostGroupDataFilter
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    # create_extra_permission_classes = (CommonPermission,)
    search_fields = ('name',)
    ordering = ['-like_count', '-share_count']
    export_field_data = ['ID', 'Tên', 'Số lượng bài viết', 'Số lượng thành viên', 'Mô tả']
    export_serializer_class = ExportPostGroupDataSerializer
