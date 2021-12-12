from django.shortcuts import render

# Create your views here.
from groups.filter import GroupDataFilter
from groups.models import Group
from groups.serializers.group import GroupDataSerializer, GroupDataCreateUpdateSerializer, \
    ExportGroupDataSerializer
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.permission.permissions import CommonPermission

# from rest_framework.request import Request


class GroupDataModelViewSet(CustomModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupDataSerializer
    create_serializer_class = GroupDataCreateUpdateSerializer
    update_serializer_class = GroupDataCreateUpdateSerializer
    filter_class = GroupDataFilter
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    # create_extra_permission_classes = (CommonPermission,)
    search_fields = ('name',)
    ordering = '-member_count'
    export_field_data = ['ID', 'Tên', 'Số lượng bài viết', 'Số lượng thành viên', 'Mô tả']
    export_serializer_class = ExportGroupDataSerializer
