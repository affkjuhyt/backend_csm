import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.vadmin.op_drf.response import SuccessResponse
from groups.models import Group
from posts.filter import PostGroupDataFilter
from posts.models import PostGroup
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.permission.permissions import CommonPermission

# from rest_framework.request import Request
from posts.serializers.post import PostGroupDataSerializer, PostGroupDataCreateUpdateSerializer, \
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

    @action(detail=False, methods=['get'], url_path='postPieChart')
    def get_post_piechart(self, request, *args, **kwargs):
        group_ids = Group.objects.filter().values_list('id')
        post = PostGroup.objects.filter().count()
        # response = {}
        list = []
        for group_id in group_ids:
            key = {}
            post_group = PostGroup.objects.filter(group_id=group_id[0]).count()
            group_name = Group.objects.filter(pk=group_id[0]).first().name
            # tag_id = Tag.objects.filter(pk__in=tag_id).first().id
            key['key'] = group_name
            key['value'] = post_group
            list.append(key)

        return SuccessResponse(data=list)

    @action(detail=False, methods=['get'], url_path='postBarChart')
    def get_post_barchart(self, request, *args, **kwargs):
        listMonth = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        book1 = PostGroup.objects.filter(date_added__lt=datetime.date(2021, 2, 1)).filter(
            date_added__gt=datetime.date(2021, 1, 1)).count()
        book2 = PostGroup.objects.filter(date_added__lt=datetime.date(2021, 3, 1)).filter(
            date_added__gt=datetime.date(2021, 2, 1)).count()
        book3 = PostGroup.objects.filter(date_added__lt=datetime.date(2021, 4, 1)).filter(
            date_added__gt=datetime.date(2021, 3, 1)).count()
        book4 = PostGroup.objects.filter(date_added__lt=datetime.date(2021, 5, 1)).filter(
            date_added__gt=datetime.date(2021, 4, 1)).count()
        book5 = PostGroup.objects.filter(date_added__lt=datetime.date(2021, 6, 1)).filter(
            date_added__gt=datetime.date(2021, 5, 1)).count()
        book6 = PostGroup.objects.filter(date_added__lt=datetime.date(2021, 7, 1)).filter(
            date_added__gt=datetime.date(2021, 6, 1)).count()
        book7 = PostGroup.objects.filter(date_added__lt=datetime.date(2021, 8, 1)).filter(
            date_added__gt=datetime.date(2021, 7, 1)).count()
        book8 = PostGroup.objects.filter(date_added__lt=datetime.date(2021, 9, 1)).filter(
            date_added__gt=datetime.date(2021, 8, 1)).count()
        book9 = PostGroup.objects.filter(date_added__lt=datetime.date(2021, 10, 1)).filter(
            date_added__gt=datetime.date(2021, 9, 1)).count()
        book10 = PostGroup.objects.filter(date_added__lt=datetime.date(2021, 11, 1)).filter(
            date_added__gt=datetime.date(2021, 10, 1)).count()
        book11 = PostGroup.objects.filter(date_added__lt=datetime.date(2021, 12, 1)).filter(
            date_added__gt=datetime.date(2021, 11, 1)).count()
        book12 = PostGroup.objects.filter(date_added__lt=datetime.date(2021, 3, 1)).filter(
            date_added__gt=datetime.date(2021, 12, 1)).count()
        list = []
        for i in listMonth:
            key = {}
            if i == 'Jan':
                key['key'] = i
                key['value'] = book1
                list.append(key)
            if i == 'Feb':
                key['key'] = i
                key['value'] = book2
                list.append(key)
            if i == 'Mar':
                key['key'] = i
                key['value'] = book3
                list.append(key)
            if i == 'Apr':
                key['key'] = i
                key['value'] = book4
                list.append(key)
            if i == 'May':
                key['key'] = i
                key['value'] = book5
                list.append(key)
            if i == 'Jun':
                key['key'] = i
                key['value'] = book6
                list.append(key)
            if i == 'Jul':
                key['key'] = i
                key['value'] = book7
                list.append(key)
            if i == 'Aug':
                key['key'] = i
                key['value'] = book8
                list.append(key)
            if i == 'Sep':
                key['key'] = i
                key['value'] = book9
                list.append(key)
            if i == 'Oct':
                key['key'] = i
                key['value'] = book10
                list.append(key)
            if i == 'Nov':
                key['key'] = i
                key['value'] = book11
                list.append(key)
            if i == 'Dec':
                key['key'] = i
                key['value'] = book12
                list.append(key)

        return SuccessResponse(data=list)
