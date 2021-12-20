from apps.vadmin.monitor.models import Server, Monitor
from apps.vadmin.op_drf.serializers import CustomModelSerializer


class ServerSerializer(CustomModelSerializer):
    class Meta:
        model = Server
        fields = ("id", "ip", "name", "os", "remark")


class UpdateServerSerializer(CustomModelSerializer):
    class Meta:
        model = Server
        fields = ("name", "remark")


class MonitorSerializer(CustomModelSerializer):
    class Meta:
        model = Monitor
        fields = '__all__'
