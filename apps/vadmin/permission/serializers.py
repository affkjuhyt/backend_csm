from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.vadmin.op_drf.serializers import CustomModelSerializer
from apps.vadmin.op_drf.validator import CustomUniqueValidator
from apps.vadmin.permission.models import Menu, Dept, Post, Role
from apps.vadmin.system.models import MessagePush

UserProfile = get_user_model()


class MenuSerializer(CustomModelSerializer):

    parentId = serializers.IntegerField(source="parentId.id", default=0)

    class Meta:
        model = Menu
        exclude = ('description', 'creator', 'modifier')


class MenuCreateUpdateSerializer(CustomModelSerializer):

    def validate(self, attrs: dict):
        return super().validate(attrs)

    def save(self, **kwargs):
        Menu.delete_cache()
        return super().save(**kwargs)

    class Meta:
        model = Menu
        fields = '__all__'


class MenuTreeSerializer(serializers.ModelSerializer):

    label = serializers.CharField(source='name', default='')
    parentId = serializers.IntegerField(source="parentId.id", default=0)

    class Meta:
        model = Menu
        fields = ('id', 'label', 'orderNum', 'parentId')


class DeptSerializer(CustomModelSerializer):

    parentId = serializers.IntegerField(source="parentId.id", default=0)

    class Meta:
        model = Dept
        exclude = ('description', 'creator', 'modifier')


class DeptCreateUpdateSerializer(CustomModelSerializer):

    def validate(self, attrs: dict):
        return super().validate(attrs)

    class Meta:
        model = Dept
        fields = '__all__'


class DeptTreeSerializer(serializers.ModelSerializer):

    label = serializers.CharField(source='deptName', default='')
    parentId = serializers.IntegerField(source="parentId.id", default=0)

    class Meta:
        model = Dept
        fields = ('id', 'label', 'parentId', 'status')


class PostSerializer(CustomModelSerializer):

    class Meta:
        model = Post
        exclude = ('description', 'creator', 'modifier')


class ExportPostSerializer(CustomModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'postName', 'postCode', 'postSort', 'status', 'creator', 'modifier', 'remark')


class PostSimpleSerializer(CustomModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'postName', 'postCode', 'status')


class PostCreateUpdateSerializer(CustomModelSerializer):

    def validate(self, attrs: dict):
        return super().validate(attrs)

    class Meta:
        model = Post
        fields = '__all__'


class RoleSerializer(CustomModelSerializer):

    class Meta:
        model = Role
        exclude = ('description', 'creator', 'modifier')


class ExportRoleSerializer(CustomModelSerializer):

    dataScope = serializers.SerializerMethodField()

    def get_dataScope(self, obj):
        dataScope = obj.get_dataScope_display()
        return dataScope

    class Meta:
        model = Role
        fields = ('id', 'roleName', 'roleKey', 'roleSort', 'dataScope', 'status', 'creator', 'modifier', 'remark')


class RoleSimpleSerializer(CustomModelSerializer):

    class Meta:
        model = Role
        fields = ('id', 'roleName', 'roleKey', 'status')


class RoleCreateUpdateSerializer(CustomModelSerializer):

    menu = MenuSerializer(many=True, read_only=True)
    dept = DeptSerializer(many=True, read_only=True)

    def validate(self, attrs: dict):
        return super().validate(attrs)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.dept.set(self.initial_data.get('dept'))
        data.menu.set(self.initial_data.get('menu'))
        return data

    class Meta:
        model = Role
        fields = '__all__'


class UserProfileDataSerializer(CustomModelSerializer):

    admin = serializers.SerializerMethodField(read_only=True)
    deptId = serializers.IntegerField(source='dept.id', read_only=True)
    unread_msg_count = serializers.SerializerMethodField(read_only=True)

    def get_admin(self, obj: UserProfile):
        role_list = obj.role.filter(status='1').values_list('admin', flat=True)
        if True in list(set(role_list)):
            return True
        return False

    def get_unread_msg_count(self, obj: UserProfile):
        return MessagePush.objects.filter(status='2').exclude(messagepushuser_message_push__is_read=True,
                                                              messagepushuser_message_push__user=obj).count()

    class Meta:
        model = UserProfile
        depth = 1
        exclude = ('password', 'secret', 'user_permissions', 'groups', 'is_superuser', 'date_joined', 'creator')


class ExportUserProfileSerializer(CustomModelSerializer):

    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    dept__deptName = serializers.CharField(source='dept.deptName', default='')
    dept__owner = serializers.CharField(source='dept.owner', default='')

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'name', 'email', 'phone_number', 'gender', 'is_active', 'last_login', 'dept__deptName',
                  'dept__owner')


class UserProfileCreateUpdateSerializer(CustomModelSerializer):

    admin = serializers.SerializerMethodField(read_only=True)
    post = PostSerializer(many=True, read_only=True)
    role = RoleSerializer(many=True, read_only=True)
    username = serializers.CharField(required=True, max_length=150,
                                     validators=[
                                         CustomUniqueValidator(queryset=UserProfile.objects.all(), message="用戶已存在")],
                                     error_messages={
                                         "blank": "Please enter username",
                                         "required": "User name cannot be empty",
                                         "max_length": "User name is too long",
                                     })

    def get_admin(self, obj: UserProfile):
        role_list = obj.role.filter(status='1').values_list('admin', flat=True)
        if True in list(set(role_list)):
            return True
        return False

    def validate(self, attrs: dict):
        return super().validate(attrs)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.role.set(self.initial_data.get('roleIds'))
        return data

    def create(self, validated_data):
        data = super().create(validated_data)
        data.set_password(self.initial_data.get('password', None))
        data.save()
        return data

    class Meta:
        model = UserProfile
        exclude = ('password', 'secret', 'user_permissions', 'groups', 'is_superuser', 'date_joined')
        read_only_fields = ('dept',)


class UserProfileImportSerializer(CustomModelSerializer):

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.set_password(self.initial_data.get('password', None))
        data.save()
        return data

    def run_validation(self, data={}):
        if type(data) is dict:
            data['role'] = str(data['role']).split(',')
            data['post'] = str(data['post']).split(',')
            data['gender'] = {'Male': '0', 'Female': '1', 'Another': '2'}.get(data['gender'])
            data['is_active'] = {'Enable': True, 'Disable': False}.get(data['is_active'])
        return super().run_validation(data)

    class Meta:
        model = UserProfile
        exclude = ('password', 'secret', 'user_permissions', 'groups', 'is_superuser', 'date_joined')
