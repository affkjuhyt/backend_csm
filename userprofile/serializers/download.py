import logging

from rest_framework import serializers

from userprofile.models import DownLoadBook

logger = logging.getLogger(__name__.split('.')[0])


class DownloadBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownLoadBook
        fields = ['id', 'chapter', 'status', 'user']
        read_only_fields = ['id']
