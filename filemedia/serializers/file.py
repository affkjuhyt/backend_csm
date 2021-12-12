import logging

from rest_framework import serializers

from filemedia.models.file import File

logger = logging.getLogger(__name__)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'posts', 'file', 'date_added', 'date_modified', 'is_deleted']
        read_only_fields = ['id']
