import datetime
import os
from datetime import date

from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from requests import Response
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from apps.vadmin.book.models import Book, Comment, Reply, TagBook, Tag
from apps.vadmin.book.serializers.book import BookDataSerializer
from apps.vadmin.op_drf.filters import DataLevelPermissionsFilter
from apps.vadmin.op_drf.response import SuccessResponse
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.permission.filters import UserProfile
from apps.vadmin.permission.permissions import CommonPermission, User
from apps.vadmin.post.models import PostGroup
from apps.vadmin.system.filters import DictDetailsFilter, DictDataFilter, ConfigSettingsFilter, MessagePushFilter, \
    SaveFileFilter, LoginInforFilter, OperationLogFilter, CeleryLogFilter
from apps.vadmin.system.models import DictData, DictDetails, ConfigSettings, SaveFile, MessagePush
from apps.vadmin.system.models import LoginInfor, OperationLog, CeleryLog
from apps.vadmin.system.models import MessagePushUser
from apps.vadmin.system.serializers import DictDataSerializer, DictDataCreateUpdateSerializer, DictDetailsSerializer, \
    DictDetailsCreateUpdateSerializer, ConfigSettingsSerializer, \
    ConfigSettingsCreateUpdateSerializer, SaveFileSerializer, SaveFileCreateUpdateSerializer, \
    ExportConfigSettingsSerializer, ExportDictDataSerializer, ExportDictDetailsSerializer, \
    MessagePushSerializer, MessagePushCreateUpdateSerializer, ExportMessagePushSerializer, LoginInforSerializer, \
    OperationLogSerializer, ExportOperationLogSerializer, ExportLoginInforSerializer, CeleryLogSerializer, \
    ExportCeleryLogSerializer
from apps.vadmin.utils.export_excel import export_excel_save_model
from apps.vadmin.utils.file_util import get_all_files, remove_empty_dir, delete_files
from apps.vadmin.utils.system_info_utils import get_memory_used_percent, get_cpu_used_percent, get_disk_used_percent


class DictDataModelViewSet(CustomModelViewSet):
    """
    字典管理模型的CRUD视图
    """
    queryset = DictData.objects.all()
    serializer_class = DictDataSerializer
    create_serializer_class = DictDataCreateUpdateSerializer
    update_serializer_class = DictDataCreateUpdateSerializer
    # list_serializer_class = ListRoleSerializer
    # retrieve_serializer_class = DetailRoleSerializer
    extra_filter_backends = [DataLevelPermissionsFilter]
    filter_class = DictDataFilter
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    search_fields = ('dictName',)
    ordering = 'id'  # 默认排序
    export_field_data = ['字典主键', '字典名称', '字典类型', '字典状态', '创建者', '修改者', '备注']
    export_serializer_class = ExportDictDataSerializer


class DictDetailsModelViewSet(CustomModelViewSet):
    """
    字典详情 模型的CRUD视图
    """
    queryset = DictDetails.objects.all()
    serializer_class = DictDetailsSerializer
    create_serializer_class = DictDetailsCreateUpdateSerializer
    update_serializer_class = DictDetailsCreateUpdateSerializer
    filter_class = DictDetailsFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    search_fields = ('dictLabel',)
    ordering = 'sort'  # 默认排序

    def dict_details_list(self, request: Request, *args, **kwargs):
        """
        根据字典类型查询字典数据信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        dict_details_dic = cache.get('system_dict_details', {}) if getattr(settings, "REDIS_ENABLE", False) else {}
        if not dict_details_dic:
            queryset = self.filter_queryset(self.get_queryset())
            queryset_dic = queryset.order_by('sort').values('dict_data__dictType', 'dictLabel', 'dictValue',
                                                            'is_default')
            for ele in queryset_dic:
                dictType = ele.pop('dict_data__dictType')
                if dictType in dict_details_dic:
                    dict_details_dic[dictType].append(ele)
                else:
                    dict_details_dic[dictType] = [ele]
            if getattr(settings, "REDIS_ENABLE", False):
                cache.set('system_dict_details', dict_details_dic, 84600)
        return SuccessResponse(dict_details_dic.get(kwargs.get('pk'), []))

    def clearCache(self, request: Request, *args, **kwargs):
        """
        清理键值缓存
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if getattr(settings, "REDIS_ENABLE", False):
            cache.delete('system_dict_details')
        return SuccessResponse(msg='清理成功！')

    def export(self, request: Request, *args, **kwargs):
        """
        导出字典详情数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        dictType = request.query_params.get('dictType')
        field_data = ['字典详情主键', '字典标签', '字典键值', '是否默认', '字典状态', '字典排序', '创建者', '修改者', '备注']
        data = ExportDictDetailsSerializer(DictDetails.objects.filter(dict_data__dictType=dictType), many=True).data
        return SuccessResponse(export_excel_save_model(request, field_data, data, f'导出字典[{dictType}]详情数据.xls'))


class ConfigSettingsModelViewSet(CustomModelViewSet):
    """
    参数设置 模型的CRUD视图
    """
    queryset = ConfigSettings.objects.all()
    serializer_class = ConfigSettingsSerializer
    create_serializer_class = ConfigSettingsCreateUpdateSerializer
    update_serializer_class = ConfigSettingsCreateUpdateSerializer
    filter_class = ConfigSettingsFilter
    search_fields = ('configName',)
    ordering = 'id'  # 默认排序
    extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    export_field_data = ['参数主键', '参数名称', '参数键名', '参数键值', '系统内置', '参数状态', '创建者', '修改者', '备注']
    export_serializer_class = ExportConfigSettingsSerializer

    def get_config_key(self, request: Request, *args, **kwargs):
        """
        根据 参数键名 查询参数数据信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        config_key_dic = cache.get('system_configKey') if getattr(settings, "REDIS_ENABLE", False) else ""
        if not config_key_dic:
            queryset = self.filter_queryset(self.get_queryset())
            config_key_dic = {ele.get('configKey'): ele.get('configValue') for ele in
                              queryset.values('configValue', 'configKey')}
            if getattr(settings, "REDIS_ENABLE", False):
                cache.set('system_configKey', config_key_dic, 84600)
        return SuccessResponse(msg=config_key_dic.get(kwargs.get('pk'), ''))

    def clearCache(self, request: Request, *args, **kwargs):
        """
        清理键值缓存
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if getattr(settings, "REDIS_ENABLE", False):
            cache.delete('system_configKey')
        return SuccessResponse(msg='清理成功！')


class SaveFileModelViewSet(CustomModelViewSet):
    """
   文件管理 模型的CRUD视图
   """
    queryset = SaveFile.objects.all()
    serializer_class = SaveFileSerializer
    create_serializer_class = SaveFileCreateUpdateSerializer
    update_serializer_class = SaveFileCreateUpdateSerializer
    filter_class = SaveFileFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    search_fields = ('configName',)
    ordering = '-create_datetime'

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return SuccessResponse(serializer.data, status=201, headers=headers)

    def clearsavefile(self, request: Request, *args, **kwargs):
        """
        清理废弃文件
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        file_list = get_all_files(os.path.join(settings.MEDIA_ROOT, 'system'))
        queryset_files = [os.path.join(os.path.join(settings.MEDIA_ROOT) + os.sep, ele) for ele in
                          list(self.get_queryset().values_list('file', flat=True))]
        queryset_files_dir = set(map(lambda absdir: os.path.abspath(absdir), queryset_files))
        delete_list = list(set(file_list) - queryset_files_dir)
        delete_files(delete_list)
        remove_empty_dir(os.path.join(settings.MEDIA_ROOT, 'system'))
        return SuccessResponse(msg=f"Dọn dẹp thành công {len(delete_list)} các tệp lỗi thời")


class MessagePushModelViewSet(CustomModelViewSet):
    """
    消息推送模型的CRUD视图
    """
    queryset = MessagePush.objects.all()
    serializer_class = MessagePushSerializer
    create_serializer_class = MessagePushCreateUpdateSerializer
    update_serializer_class = MessagePushCreateUpdateSerializer
    # extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    filter_class = MessagePushFilter
    ordering = "-update_datetime"  # 默认排序
    export_field_data = ['消息序号', '标题', '内容', '消息类型', '是否审核', '消息状态', '通知接收消息用户',
                         '创建者', '修改者', '修改时间', '创建时间']
    export_serializer_class = ExportMessagePushSerializer

    def get_user_messages(self, request: Request, *args, **kwargs):
        """
        获取用户自己消息列表
        """
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(status=2)
        is_read = request.query_params.get('is_read', None)
        if is_read:
            if is_read == 'False':
                queryset = queryset.exclude(Q(messagepushuser_message_push__is_read=True),
                                            Q(messagepushuser_message_push__user=request.user))
            elif is_read == 'True':
                queryset = queryset.filter(messagepushuser_message_push__is_read=True,
                                           messagepushuser_message_push__user=request.user)
        queryset = queryset.filter(is_reviewed=True).distinct()
        page = self.paginate_queryset(queryset)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        if page is not None:
            if getattr(self, 'values_queryset', None):
                return self.get_paginated_response(page)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        if getattr(self, 'values_queryset', None):
            return SuccessResponse(page)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(serializer.data)

    def update_is_read(self, request: Request, *args, **kwargs):
        """
        修改为已读
        """
        instance, _ = MessagePushUser.objects.get_or_create(message_push_id=kwargs.get('pk'), user=request.user)
        instance.is_read = True
        instance.save()
        return SuccessResponse()


class LoginInforModelViewSet(CustomModelViewSet):
    """
   登录日志 模型的CRUD视图
   """
    queryset = LoginInfor.objects.all()
    serializer_class = LoginInforSerializer
    filter_class = LoginInforFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    ordering = '-create_datetime'  # 默认排序
    export_field_data = ['访问编号', '用户名称', '登录地址', '登录地点', '浏览器', '操作系统',
                         '登录状态', '操作信息', '登录日期']
    export_serializer_class = ExportLoginInforSerializer

    def clean_all(self, request: Request, *args, **kwargs):
        """
        清空登录日志
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.get_queryset().delete()
        return SuccessResponse(msg="清空成功")


class OperationLogModelViewSet(CustomModelViewSet):
    """
   操作日志 模型的CRUD视图
   """
    queryset = OperationLog.objects.all()
    serializer_class = OperationLogSerializer
    filter_class = OperationLogFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    ordering = '-create_datetime'  # 默认排序
    export_field_data = ['请求模块', '请求地址', '请求参数', '请求方式', '操作说明', '请求ip地址',
                         '请求浏览器', '响应状态码', '操作地点', '操作系统', '返回信息', '响应状态', '操作用户名']
    export_serializer_class = ExportOperationLogSerializer

    def clean_all(self, request: Request, *args, **kwargs):
        """
        清空操作日志
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.get_queryset().delete()
        return SuccessResponse(msg="清空成功")


class CeleryLogModelViewSet(CustomModelViewSet):
    queryset = CeleryLog.objects.all()
    serializer_class = CeleryLogSerializer
    extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    filter_class = CeleryLogFilter
    ordering = '-create_datetime'  # 默认排序
    export_field_data = ['任务名称', '执行参数', '执行时间', '运行状态', '任务结果', '创建时间']
    export_serializer_class = ExportCeleryLogSerializer

    def clean_all(self, request: Request, *args, **kwargs):
        self.get_queryset().delete()
        return SuccessResponse(msg="清空成功")


class SystemInfoApiView(APIView):

    def get(self, request, *args, **kwargs):
        memory_used_percent = get_memory_used_percent()
        cpu_used_percent = get_cpu_used_percent()
        disk_used_percent = get_disk_used_percent()
        return SuccessResponse(data={"memory_used_percent": memory_used_percent,
                                     "cpu_used_percent": cpu_used_percent,
                                     "disk_used_percent": disk_used_percent
                                     })


class DashboardApiView(APIView):
    def get(self, request, *args, **kwargs):
        result = Book.objects.filter().count()
        comment = Comment.objects.filter().count()
        reply = Reply.objects.filter().count()
        result1 = comment + reply
        user = User.objects.filter().count()
        post = PostGroup.objects.filter().count()
        return SuccessResponse(data={"count_book": result,
                                     "count_comment": result1,
                                     "count_user": user,
                                     "count_post": post})


class PieChartApiView(APIView):
    def get(self, request, *args, **kwargs):
        tag_ids = Tag.objects.filter().values_list('id')
        book = Book.objects.filter().count()
        # response = {}
        list = []
        for tag_id in tag_ids:
            key = {}
            tag_book = TagBook.objects.filter(tag=tag_id).count()
            tag_name = Tag.objects.filter(pk__in=tag_id).first().name
            # tag_id = Tag.objects.filter(pk__in=tag_id).first().id
            key['key'] = tag_name
            key['value'] = tag_book
            list.append(key)
            # list
            # response.update(key)

        return SuccessResponse(data=list)


class BarChartApiView(APIView):
    def get(self, request, *args, **kwargs):
        response = {}
        # Get ra 3 truyen co so like nhieu nhat
        book = Book.objects.filter().order_by('-like_count')[:3]
        response['bookA'] = book[0].title
        response['bookB'] = book[1].title
        response['bookC'] = book[2].title

        return SuccessResponse(data=response)


class GetCommentDayView(APIView):
    def get(self, request, *args, **kwargs):
        response = {}
        today = datetime.datetime.today().weekday()
        response['Mon'] = PostGroup.objects.filter(
            create_datetime__gte=(datetime.datetime.now() - datetime.timedelta(days=today))).count()
        response['Tue'] = PostGroup.objects.filter(
            create_datetime__gte=datetime.datetime.now() - datetime.timedelta(days=today) + datetime.timedelta(
                days=1)).count()
        response['Wed'] = PostGroup.objects.filter(
            create_datetime__gte=datetime.datetime.now() - datetime.timedelta(days=today) + datetime.timedelta(
                days=2)).count()
        response['Thu'] = PostGroup.objects.filter(
            create_datetime__gte=datetime.datetime.now() - datetime.timedelta(days=today) + datetime.timedelta(
                days=3)).count()
        response['Fri'] = PostGroup.objects.filter(
            create_datetime__gte=datetime.datetime.now() - datetime.timedelta(days=today) + datetime.timedelta(
                days=4)).count()
        response['Sat'] = PostGroup.objects.filter(
            create_datetime__gte=datetime.datetime.now() - datetime.timedelta(days=today) + datetime.timedelta(
                days=5)).count()
        response['Sun'] = PostGroup.objects.filter(
            create_datetime__gte=datetime.datetime.now() - datetime.timedelta(days=today) + datetime.timedelta(
                days=6)).count()

        return SuccessResponse(data=response)
