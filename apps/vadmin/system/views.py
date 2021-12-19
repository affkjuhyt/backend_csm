import datetime
import os

from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.vadmin.permission.models import UserProfile, Role
from books.models import Book, Comment, Reply, TagBook, Tag
from apps.vadmin.op_drf.filters import DataLevelPermissionsFilter
from apps.vadmin.op_drf.response import SuccessResponse
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.permission.permissions import CommonPermission, User
from posts.models import PostGroup
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
    ordering = 'id'
    export_field_data = ['字典主键', '字典名称', '字典类型', '字典状态', '创建者', '修改者', '备注']
    export_serializer_class = ExportDictDataSerializer


class DictDetailsModelViewSet(CustomModelViewSet):
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
    ordering = 'sort'

    def dict_details_list(self, request: Request, *args, **kwargs):
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
        if getattr(settings, "REDIS_ENABLE", False):
            cache.delete('system_dict_details')
        return SuccessResponse(msg='清理成功！')

    def export(self, request: Request, *args, **kwargs):
        dictType = request.query_params.get('dictType')
        field_data = ['字典详情主键', '字典标签', '字典键值', '是否默认', '字典状态', '字典排序', '创建者', '修改者', '备注']
        data = ExportDictDetailsSerializer(DictDetails.objects.filter(dict_data__dictType=dictType), many=True).data
        return SuccessResponse(export_excel_save_model(request, field_data, data, f'导出字典[{dictType}]详情数据.xls'))


class ConfigSettingsModelViewSet(CustomModelViewSet):
    queryset = ConfigSettings.objects.all()
    serializer_class = ConfigSettingsSerializer
    create_serializer_class = ConfigSettingsCreateUpdateSerializer
    update_serializer_class = ConfigSettingsCreateUpdateSerializer
    filter_class = ConfigSettingsFilter
    search_fields = ('configName',)
    ordering = 'id'
    extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    export_field_data = ['参数主键', '参数名称', '参数键名', '参数键值', '系统内置', '参数状态', '创建者', '修改者', '备注']
    export_serializer_class = ExportConfigSettingsSerializer

    def get_config_key(self, request: Request, *args, **kwargs):
        config_key_dic = cache.get('system_configKey') if getattr(settings, "REDIS_ENABLE", False) else ""
        if not config_key_dic:
            queryset = self.filter_queryset(self.get_queryset())
            config_key_dic = {ele.get('configKey'): ele.get('configValue') for ele in
                              queryset.values('configValue', 'configKey')}
            if getattr(settings, "REDIS_ENABLE", False):
                cache.set('system_configKey', config_key_dic, 84600)
        return SuccessResponse(msg=config_key_dic.get(kwargs.get('pk'), ''))

    def clearCache(self, request: Request, *args, **kwargs):
        if getattr(settings, "REDIS_ENABLE", False):
            cache.delete('system_configKey')
        return SuccessResponse(msg='清理成功！')


class SaveFileModelViewSet(CustomModelViewSet):
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
        file_list = get_all_files(os.path.join(settings.MEDIA_ROOT, 'system'))
        queryset_files = [os.path.join(os.path.join(settings.MEDIA_ROOT) + os.sep, ele) for ele in
                          list(self.get_queryset().values_list('file', flat=True))]
        queryset_files_dir = set(map(lambda absdir: os.path.abspath(absdir), queryset_files))
        delete_list = list(set(file_list) - queryset_files_dir)
        delete_files(delete_list)
        remove_empty_dir(os.path.join(settings.MEDIA_ROOT, 'system'))
        return SuccessResponse(msg=f"Dọn dẹp thành công {len(delete_list)} các tệp lỗi thời")


class MessagePushModelViewSet(CustomModelViewSet):
    queryset = MessagePush.objects.all()
    serializer_class = MessagePushSerializer
    create_serializer_class = MessagePushCreateUpdateSerializer
    update_serializer_class = MessagePushCreateUpdateSerializer
    # extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    filter_class = MessagePushFilter
    ordering = "-update_datetime"
    export_field_data = ['消息序号', '标题', '内容', '消息类型', '是否审核', '消息状态', '通知接收消息用户',
                         '创建者', '修改者', '修改时间', '创建时间']
    export_serializer_class = ExportMessagePushSerializer

    def get_user_messages(self, request: Request, *args, **kwargs):
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
        instance, _ = MessagePushUser.objects.get_or_create(message_push_id=kwargs.get('pk'), user=request.user)
        instance.is_read = True
        instance.save()
        return SuccessResponse()


class LoginInforModelViewSet(CustomModelViewSet):
    queryset = LoginInfor.objects.all()
    serializer_class = LoginInforSerializer
    filter_class = LoginInforFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    ordering = '-create_datetime'
    export_field_data = ['访问编号', '用户名称', '登录地址', '登录地点', '浏览器', '操作系统',
                         '登录状态', '操作信息', '登录日期']
    export_serializer_class = ExportLoginInforSerializer

    def clean_all(self, request: Request, *args, **kwargs):
        self.get_queryset().delete()
        return SuccessResponse(msg="清空成功")


class OperationLogModelViewSet(CustomModelViewSet):
    queryset = OperationLog.objects.all()
    serializer_class = OperationLogSerializer
    filter_class = OperationLogFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    ordering = '-create_datetime'
    export_field_data = ['请求模块', '请求地址', '请求参数', '请求方式', '操作说明', '请求ip地址',
                         '请求浏览器', '响应状态码', '操作地点', '操作系统', '返回信息', '响应状态', '操作用户名']
    export_serializer_class = ExportOperationLogSerializer

    def clean_all(self, request: Request, *args, **kwargs):
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
    ordering = '-create_datetime'
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


class PercentUserApiView(APIView):
    def get(self, request: Request, *args, **kwargs):
        user = UserProfile.objects.all()
        list = []
        x = range(2, 4)
        for i in x:
            key = {}
            role = Role.objects.filter(id=i).first()
            key["key"] = role.roleName
            key["value"] = user.filter(role=role).count()
            list.append(key)
        return SuccessResponse(data=list)


class RegisterUserApiView(APIView):
    def get(self, request, *args, **kwargs):
        listMonth = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        book1 = UserProfile.objects.filter(create_datetime__lt=datetime.date(2021, 2, 1)).filter(
            create_datetime__gt=datetime.date(2021, 1, 1)).count()
        book2 = UserProfile.objects.filter(create_datetime__lt=datetime.date(2021, 3, 1)).filter(
            create_datetime__gt=datetime.date(2021, 2, 1)).count()
        book3 = UserProfile.objects.filter(create_datetime__lt=datetime.date(2021, 4, 1)).filter(
            create_datetime__gt=datetime.date(2021, 3, 1)).count()
        book4 = UserProfile.objects.filter(create_datetime__lt=datetime.date(2021, 5, 1)).filter(
            create_datetime__gt=datetime.date(2021, 4, 1)).count()
        book5 = UserProfile.objects.filter(create_datetime__lt=datetime.date(2021, 6, 1)).filter(
            create_datetime__gt=datetime.date(2021, 5, 1)).count()
        book6 = UserProfile.objects.filter(create_datetime__lt=datetime.date(2021, 7, 1)).filter(
            create_datetime__gt=datetime.date(2021, 6, 1)).count()
        book7 = UserProfile.objects.filter(create_datetime__lt=datetime.date(2021, 8, 1)).filter(
            create_datetime__gt=datetime.date(2021, 7, 1)).count()
        book8 = UserProfile.objects.filter(create_datetime__lt=datetime.date(2021, 9, 1)).filter(
            create_datetime__gt=datetime.date(2021, 8, 1)).count()
        book9 = UserProfile.objects.filter(create_datetime__lt=datetime.date(2021, 10, 1)).filter(
            create_datetime__gt=datetime.date(2021, 9, 1)).count()
        book10 = UserProfile.objects.filter(create_datetime__lt=datetime.date(2021, 11, 1)).filter(
            create_datetime__gt=datetime.date(2021, 10, 1)).count()
        book11 = UserProfile.objects.filter(create_datetime__lt=datetime.date(2021, 12, 1)).filter(
            create_datetime__gt=datetime.date(2021, 11, 1)).count()
        book12 = UserProfile.objects.filter(create_datetime__lt=datetime.date(2022, 1, 1)).filter(
            create_datetime__gt=datetime.date(2021, 12, 1)).count()
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

class BookBarChartView(APIView):
    def get(self, request, *args, **kwargs):
        listMonth = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        book1 = Book.objects.filter(date_added__lt=datetime.date(2021, 2, 1)).filter(
            date_added__gt=datetime.date(2021, 1, 1)).count()
        book2 = Book.objects.filter(date_added__lt=datetime.date(2021, 3, 1)).filter(
            date_added__lt=datetime.date(2021, 2, 28)).count()
        book3 = Book.objects.filter(date_added__lt=datetime.date(2021, 4, 1)).filter(
            date_added__lt=datetime.date(2021, 3, 31)).count()
        book4 = Book.objects.filter(date_added__lt=datetime.date(2021, 5, 1)).filter(
            date_added__lt=datetime.date(2021, 4, 30)).count()
        book5 = Book.objects.filter(date_added__lt=datetime.date(2021, 6, 1)).filter(
            date_added__lt=datetime.date(2021, 5, 31)).count()
        book6 = Book.objects.filter(date_added__lt=datetime.date(2021, 7, 1)).filter(
            date_added__lt=datetime.date(2021, 6, 30)).count()
        book7 = Book.objects.filter(date_added__lt=datetime.date(2021, 8, 1)).filter(
            date_added__lt=datetime.date(2021, 7, 31)).count()
        book8 = Book.objects.filter(date_added__lt=datetime.date(2021, 9, 1)).filter(
            date_added__lt=datetime.date(2021, 8, 31)).count()
        book9 = Book.objects.filter(date_added__lt=datetime.date(2021, 10, 1)).filter(
            date_added__lt=datetime.date(2021, 9, 30)).count()
        book10 = Book.objects.filter(date_added__lt=datetime.date(2021, 11, 1)).filter(
            date_added__lt=datetime.date(2021, 10, 31)).count()
        book11 = Book.objects.filter(date_added__lt=datetime.date(2021, 12, 1)).filter(
            date_added__lt=datetime.date(2021, 11, 30)).count()
        book12 = Book.objects.filter(date_added__lt=datetime.date(2021, 3, 1)).filter(
            date_added__lt=datetime.date(2021, 12, 31)).count()
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
        listMonth = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        book1 = OperationLog.objects.filter(create_datetime__lt=datetime.date(2021, 2, 1)).filter(
            create_datetime__gt=datetime.date(2021, 1, 1)).count()
        book2 = OperationLog.objects.filter(create_datetime__lt=datetime.date(2021, 3, 1)).filter(
            create_datetime__lt=datetime.date(2021, 2, 28)).count()
        book3 = OperationLog.objects.filter(create_datetime__lt=datetime.date(2021, 4, 1)).filter(
            create_datetime__lt=datetime.date(2021, 3, 31)).count()
        book4 = OperationLog.objects.filter(create_datetime__lt=datetime.date(2021, 5, 1)).filter(
            create_datetime__lt=datetime.date(2021, 4, 30)).count()
        book5 = OperationLog.objects.filter(create_datetime__lt=datetime.date(2021, 6, 1)).filter(
            create_datetime__lt=datetime.date(2021, 5, 31)).count()
        book6 = OperationLog.objects.filter(create_datetime__lt=datetime.date(2021, 7, 1)).filter(
            create_datetime__lt=datetime.date(2021, 6, 30)).count()
        book7 = OperationLog.objects.filter(create_datetime__lt=datetime.date(2021, 8, 1)).filter(
            create_datetime__lt=datetime.date(2021, 7, 31)).count()
        book8 = OperationLog.objects.filter(create_datetime__lt=datetime.date(2021, 9, 1)).filter(
            create_datetime__lt=datetime.date(2021, 8, 31)).count()
        book9 = OperationLog.objects.filter(create_datetime__lt=datetime.date(2021, 10, 1)).filter(
            create_datetime__lt=datetime.date(2021, 9, 30)).count()
        book10 = OperationLog.objects.filter(create_datetime__lt=datetime.date(2021, 11, 1)).filter(
            create_datetime__lt=datetime.date(2021, 10, 31)).count()
        book11 = OperationLog.objects.filter(create_datetime__lt=datetime.date(2021, 12, 1)).filter(
            create_datetime__lt=datetime.date(2021, 11, 30)).count()
        book12 = OperationLog.objects.filter(create_datetime__lt=datetime.date(2021, 3, 1)).filter(
            create_datetime__lt=datetime.date(2021, 12, 31)).count()
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


class GetCommentDayView(APIView):
    def get(self, request, *args, **kwargs):
        response = {}
        today = datetime.datetime.today().weekday()
        response['Mon'] = PostGroup.objects.filter(
            date_added__gte=(datetime.datetime.now() - datetime.timedelta(days=today))).count()
        response['Tue'] = PostGroup.objects.filter(
            date_added__gte=datetime.datetime.now() - datetime.timedelta(days=today) + datetime.timedelta(
                days=1)).count()
        response['Wed'] = PostGroup.objects.filter(
            date_added__gte=datetime.datetime.now() - datetime.timedelta(days=today) + datetime.timedelta(
                days=2)).count()
        response['Thu'] = PostGroup.objects.filter(
            date_added__gte=datetime.datetime.now() - datetime.timedelta(days=today) + datetime.timedelta(
                days=3)).count()
        response['Fri'] = PostGroup.objects.filter(
            date_added__gte=datetime.datetime.now() - datetime.timedelta(days=today) + datetime.timedelta(
                days=4)).count()
        response['Sat'] = PostGroup.objects.filter(
            date_added__gte=datetime.datetime.now() - datetime.timedelta(days=today) + datetime.timedelta(
                days=5)).count()
        response['Sun'] = PostGroup.objects.filter(
            date_added__gte=datetime.datetime.now() - datetime.timedelta(days=today) + datetime.timedelta(
                days=6)).count()

        return SuccessResponse(data=response)
