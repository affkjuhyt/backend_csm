import logging

from rest_framework import serializers

from apps.vadmin.op_drf.serializers import CustomModelSerializer
from books.models import VulgarWord

logger = logging.getLogger(__name__.split('.')[0])


class VulgarWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VulgarWord
        fields = ['id', 'word', 're_word']
        read_only_fields = ['id']


class VulgarDataSerializer(CustomModelSerializer):
    """
    VulgarDataSerializer
    """

    class Meta:
        model = VulgarWord
        fields = '__all__'


class VulgarDataCreateUpdateSerializer(CustomModelSerializer):
    """
    VulgarCreateSerializer
    """

    class Meta:
        model = VulgarWord
        fields = '__all__'


class ExportVulgarDataSerializer(CustomModelSerializer):
    """
    ExportVulgarData
    """

    class Meta:
        model = VulgarWord
        fields = ('id', 'word', 're_word')
