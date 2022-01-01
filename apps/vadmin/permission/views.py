from django.contrib.auth import authenticate, get_user_model
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.vadmin.op_drf.response import SuccessResponse, ErrorResponse
from apps.vadmin.permission.permissions import CommonPermission, DeptDestroyPermission
from apps.vadmin.op_drf.filters import DataLevelPermissionsFilter
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.permission.filters import MenuFilter, DeptFilter, PostFilter, RoleFilter, UserProfileFilter
from apps.vadmin.permission.models import Role, Menu, Dept, Post
from apps.vadmin.permission.serializers import UserProfileDataSerializer, MenuSerializer, RoleSerializer, \
    MenuCreateUpdateSerializer, DeptSerializer, DeptCreateUpdateSerializer, PostCreateUpdateSerializer, \
    RoleCreateUpdateSerializer, DeptTreeSerializer, MenuTreeSerializer, UserProfileCreateUpdateSerializer, \
    PostSimpleSerializer, RoleSimpleSerializer, ExportUserProfileSerializer, ExportRoleSerializer, ExportPostSerializer, \
    UserProfileImportSerializer
from apps.vadmin.system.models import DictDetails

UserProfile = get_user_model()


class GetUserProfileView(APIView):
    def get(self, request, format=None):
        user_dict = UserProfileDataSerializer(request.user).data
        permissions_list = ['*:*:*'] if user_dict.get('admin') else Menu.objects.filter(
            role__userprofile=request.user).values_list('perms', flat=True)
        # delete_cache = request.user.delete_cache
        return SuccessResponse({
            'permissions': [ele for ele in permissions_list if ele],
            'roles': Role.objects.filter(userprofile=request.user).values_list('roleKey', flat=True),
            'user': user_dict
        })


class GetRouters(APIView):
    def depth_menu(self, menus):
        return dict

    def get(self, request, format=None):
        kwargs = {}
        if not request.user.is_superuser:
            kwargs['role__userprofile'] = request.user
        menus = Menu.objects.filter(**kwargs) \
            .exclude(menuType='2').values('id', 'name', 'web_path', 'visible', 'status', 'isFrame', 'component_path',
                                          'icon', 'parentId', 'orderNum', 'isCache').distinct()
        data = []
        sys_show_hide = DictDetails.get_default_dictValue('sys_show_hide')
        for ele in menus:
            data.append({
                'id': ele.get('id'),
                'name': ele.get('web_path', '').split('/')[-1] and ele.get('web_path', '').split('/')[-1].capitalize(),
                'path': ele.get('web_path'),
                'orderNum': ele.get('orderNum'),
                'hidden': True if ele.get('visible') != '1' else False,
                'redirect': ele.get('web_path') if ele.get('isFrame') == '1' else 'noRedirect',
                'component': ele.get('component_path') or 'Layout',
                'meta': {'title': ele.get('name'), 'icon': ele.get('icon'),
                         'noCache': True if ele.get('isCache') == sys_show_hide else False},
                'parentId': ele.get('parentId')
            })
        return SuccessResponse(data)


class MenuModelViewSet(CustomModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    create_serializer_class = MenuCreateUpdateSerializer
    update_serializer_class = MenuCreateUpdateSerializer
    filter_class = MenuFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    search_fields = ('name',)
    ordering = 'create_datetime'

    def tree_select_list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        serializer = MenuTreeSerializer(queryset, many=True)
        return SuccessResponse(serializer.data)

    def role_menu_tree_select(self, request: Request, *args, **kwargs):
        menu_queryset = Menu.objects.filter(role__id=kwargs.get('pk')).values_list('id', flat=True)
        queryset = self.filter_queryset(self.get_queryset())
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        serializer = MenuTreeSerializer(queryset, many=True)
        return SuccessResponse({
            'menus': serializer.data,
            'checkedKeys': menu_queryset
        })


class DeptModelViewSet(CustomModelViewSet):
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer
    create_serializer_class = DeptCreateUpdateSerializer
    update_serializer_class = DeptCreateUpdateSerializer
    filter_class = DeptFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission, DeptDestroyPermission)
    create_extra_permission_classes = (CommonPermission,)
    search_fields = ('deptName',)
    ordering = 'create_datetime'

    def exclude_list(self, request: Request, *args, **kwargs):
        dept_queryset = Dept.objects.filter(id=kwargs.get('pk')).first()
        parentId = dept_queryset.parentId if dept_queryset else ''
        queryset = self.queryset.exclude(parentId=parentId).order_by('orderNum')
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(serializer.data)

    def tree_select_list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        serializer = DeptTreeSerializer(queryset, many=True)
        return SuccessResponse(serializer.data)

    def role_dept_tree_select(self, request: Request, *args, **kwargs):
        dept_queryset = Dept.objects.filter(role__id=kwargs.get('pk')).values_list('id', flat=True)
        queryset = self.filter_queryset(self.get_queryset())
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        serializer = DeptTreeSerializer(queryset, many=True)
        return SuccessResponse({
            'depts': serializer.data,
            'checkedKeys': dept_queryset
        })


class RoleModelViewSet(CustomModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    create_serializer_class = RoleCreateUpdateSerializer
    update_serializer_class = RoleCreateUpdateSerializer
    filter_class = RoleFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    search_fields = ('roleName',)
    ordering = 'create_datetime'
    export_field_data = ['STT', 'Tên vai trò', 'Quyền của vai trò', 'Xếp hạng', 'Phạm vi', 'Tình trạng', 'Người tạo', 'Người biên tập', 'Nhận xét']
    export_serializer_class = ExportRoleSerializer


class UserProfileModelViewSet(CustomModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDataSerializer
    create_serializer_class = UserProfileCreateUpdateSerializer
    update_serializer_class = UserProfileCreateUpdateSerializer
    filter_class = UserProfileFilter
    export_serializer_class = ExportUserProfileSerializer
    export_field_data = ['ID', 'Username', 'Name', 'Email', 'Phone', 'Gender', 'Status', 'LastLogin']
    import_serializer_class = UserProfileImportSerializer
    import_field_data = {'username': 'Tài khoản', 'name': 'Tên', 'email': 'Email', 'mobile': 'SĐT',
                         'gender': 'Giới tính',
                         'is_active': 'Trạng thái tài khoản', 'password': 'Mật khẩu', 'role': 'role',
                         'post': 'post'}
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    search_fields = ('username',)
    ordering = 'create_datetime'

    def change_status(self, request: Request, *args, **kwargs):
        instance = self.queryset.get(id=request.data.get('userId'))
        instance.is_active = request.data.get('status')
        instance.save()
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)

    def get_user_details(self, request: Request, *args, **kwargs):
        userId = request.query_params.get('userId')
        data = {
            'posts': PostSimpleSerializer(Post.objects.filter(status='1').order_by('postSort'), many=True).data,
            'roles': RoleSimpleSerializer(Role.objects.filter(status='1').order_by('roleSort'), many=True).data
        }
        if userId:
            instance = self.queryset.get(id=userId)
            serializer = self.get_serializer(instance)
            data['data'] = serializer.data
            data['roleIds'] = [ele.get('id') for ele in serializer.data.get('role')]
            if hasattr(self, 'handle_logging'):
                self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(data)

    def reset_pwd(self, request: Request, *args, **kwargs):
        instance = self.queryset.get(id=request.data.get('userId'))
        serializer = self.get_serializer(instance)
        instance.set_password(request.data.get('password'))
        instance.save()
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)

    def profile(self, request: Request, *args, **kwargs):
        instance = self.queryset.get(id=request.user.id)
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)

    def put_profile(self, request: Request, *args, **kwargs):
        instance = self.queryset.get(id=request.user.id)
        instance.name = request.data.get('name', None)
        instance.mobile = request.data.get('mobile', None)
        instance.email = request.data.get('email', None)
        instance.gender = request.data.get('gender', None)
        instance.save()
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)

    def put_avatar(self, request: Request, *args, **kwargs):
        instance = self.queryset.get(id=request.user.id)
        instance.avatar = request.data.get('avatar_url', None)
        instance.save()
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)

    def update_pwd(self, request: Request, *args, **kwargs):
        instance = self.queryset.get(id=request.user.id)
        instance.password = request.data.get('newPassword', None)
        if not authenticate(username=request.user.username, password=request.data.get('oldPassword', None)):
            return ErrorResponse(msg='Mật khẩu cũ không dúng！')
        instance.set_password(request.data.get('newPassword'))
        instance.save()
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)
