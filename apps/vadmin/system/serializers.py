from django.core.cache import cache
from rest_framework import serializers

from application import settings
from apps.vadmin.op_drf.serializers import CustomModelSerializer
from apps.vadmin.system.models import DictData, DictDetails, ConfigSettings, SaveFile, MessagePush, MessagePushUser
from apps.vadmin.system.models import LoginInfor, OperationLog, CeleryLog


class DictDataSerializer(CustomModelSerializer):

    class Meta:
        model = DictData
        exclude = ('description', 'creator', 'modifier')


class ExportDictDataSerializer(CustomModelSerializer):
    class Meta:
        model = DictData
        fields = ('id', 'dictName', 'dictType', 'status', 'creator', 'modifier', 'remark',)


class DictDataCreateUpdateSerializer(CustomModelSerializer):

    class Meta:
        model = DictData
        fields = '__all__'


class DictDetailsSerializer(CustomModelSerializer):
    dictType = serializers.CharField(source='dict_data.dictType', default='', read_only=True)

    class Meta:
        model = DictDetails
        exclude = ('description', 'creator', 'modifier')


class ExportDictDetailsSerializer(CustomModelSerializer):
    class Meta:
        model = DictDetails
        fields = ('id', 'dictLabel', 'dictValue', 'is_default', 'status', 'sort', 'creator', 'modifier', 'remark',)


class DictDetailsListSerializer(CustomModelSerializer):

    class Meta:
        model = DictDetails
        fields = ('dictLabel', 'dictValue', 'is_default')


class DictDetailsCreateUpdateSerializer(CustomModelSerializer):

    def save(self, **kwargs):
        if getattr(settings, "REDIS_ENABLE", False):
            cache.delete('system_dict_details')
        return super().save(**kwargs)

    class Meta:
        model = DictDetails
        fields = '__all__'


class ConfigSettingsSerializer(CustomModelSerializer):

    class Meta:
        model = ConfigSettings
        exclude = ('description', 'creator', 'modifier')


class ExportConfigSettingsSerializer(CustomModelSerializer):

    class Meta:
        model = ConfigSettings
        fields = (
            'id', 'configName', 'configKey', 'configValue', 'configType', 'status', 'creator', 'modifier', 'remark')


class ConfigSettingsCreateUpdateSerializer(CustomModelSerializer):

    def save(self, **kwargs):
        if getattr(settings, "REDIS_ENABLE", False):
            cache.delete('system_configKey')
        return super().save(**kwargs)

    class Meta:
        model = ConfigSettings
        fields = '__all__'


class SaveFileSerializer(CustomModelSerializer):
    file_url = serializers.CharField(source='file.url', read_only=True)

    class Meta:
        model = SaveFile
        exclude = ('description',)


class SaveFileCreateUpdateSerializer(CustomModelSerializer):
    file_url = serializers.SerializerMethodField(read_only=True)

    def get_file_url(self, obj: SaveFile):
        return getattr(obj.file, "url", obj.file) if hasattr(obj, "file") else ""

    def save(self, **kwargs):
        files = self.context.get('request').FILES.get('file')
        self.validated_data['name'] = files.name
        self.validated_data['size'] = files.size
        self.validated_data['type'] = files.content_type
        self.validated_data['address'] = 'lưu trữ cục bộ'
        self.validated_data['source'] = 'Người dùng tải lên'
        instance = super().save(**kwargs)
        return instance

    class Meta:
        model = SaveFile
        fields = '__all__'


class MessagePushSerializer(CustomModelSerializer):

    class Meta:
        model = MessagePush
        fields = "__all__"

    def save(self, **kwargs):
        return super().save(**kwargs)


class MessagePushCreateUpdateSerializer(CustomModelSerializer):

    class Meta:
        model = MessagePush
        fields = "__all__"


class ExportMessagePushSerializer(CustomModelSerializer):

    users = serializers.CharField(read_only=True)

    def get_users(self, obj):
        return ','.join(MessagePush.objects.filter(id=obj.id).values_list('user__username', flat=True))

    class Meta:
        model = MessagePush
        fields = (
            'id', 'title', 'content', 'message_type', 'is_reviewed', 'status', 'users', 'creator', 'modifier',
            'update_datetime', 'create_datetime')


class MessagePushUserSerializer(CustomModelSerializer):

    # users = UserProfileSerializer(read_only=True)
    # users = serializers.SerializerMethodField(read_only=True)
    is_read = serializers.SerializerMethodField(read_only=True)

    # def get_users(self, obj):
    #     return UserProfileSerializer(obj.user.all(), many=True).data
    def get_is_read(self, obj):
        object = MessagePushUser.objects.filter(message_push=obj, user=self.context.get('request').user).first()
        return object.is_read if object else False

    class Meta:
        model = MessagePush
        fields = "__all__"

    def save(self, **kwargs):
        return super().save(**kwargs)


class LoginInforSerializer(CustomModelSerializer):

    class Meta:
        model = LoginInfor
        fields = "__all__"


class ExportLoginInforSerializer(CustomModelSerializer):

    class Meta:
        model = LoginInfor
        fields = ('id', 'creator_name', 'ipaddr', 'loginLocation', 'browser', 'os',
                  'status', 'msg')


class OperationLogSerializer(CustomModelSerializer):

    class Meta:
        model = OperationLog
        fields = "__all__"


class ExportOperationLogSerializer(CustomModelSerializer):

    class Meta:
        model = OperationLog
        fields = ('request_modular', 'request_path', 'request_body', 'request_method', 'request_msg', 'request_ip',
                  'request_browser', 'response_code', 'request_location', 'request_os', 'json_result', 'status',
                  'creator_name')


class CeleryLogSerializer(CustomModelSerializer):

    class Meta:
        model = CeleryLog
        fields = "__all__"


class ExportCeleryLogSerializer(CustomModelSerializer):

    class Meta:
        model = CeleryLog
        fields = ('name', 'kwargs', 'seconds', 'status', 'result', 'creator_name')
