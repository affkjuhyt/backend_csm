import logging

from rest_framework import serializers

from apps.vadmin.op_drf.serializers import CustomModelSerializer
from books.models import Chapter, Image, Comment, Reply
from books.serializers.image import ImageSerializer
from userprofile.models import DownLoadBook

logger = logging.getLogger(__name__)

from datetime import datetime
today = datetime.now()
today_path = today.strftime("%Y/%m/%d")


class ChapterSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ['id', 'book', 'number', 'title', 'thumbnail', 'date_modified',
                  'date_added', 'like_count', 'is_deleted', 'images', 'size']
        read_only_fields = ['id']

    def get_images(self, obj):
        image = Image.objects.filter(chapter=obj.id)
        return ImageSerializer(image, many=True).data

    def get_size(self, obj):
        images = Image.objects.filter(chapter=obj.id)
        size_bytes = 0
        for image in images:
            size_bytes += image.image.size
        mb_size = size_bytes / 1048574
        return mb_size

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if self.context == {}:
            return response
        else:
            user = self.context.get('request').user
            if user.id == None:
                pass
            else:
                chapter_ids = DownLoadBook.objects.filter(user=user).filter(chapter=instance).exclude(
                    status=[DownLoadBook.NOT_DOWNLOAD]).values_list('chapter_id', flat=True)
                if instance.id in chapter_ids:
                    chapter_downloaded = DownLoadBook.objects.filter(user=user).filter(chapter=instance).exclude(
                        status=[DownLoadBook.NOT_DOWNLOAD, DownLoadBook.ERROR]).first()
                    response['status_download'] = chapter_downloaded.status
                else:
                    response['status_download'] = DownLoadBook.NOT_DOWNLOAD

            return response


class ChapterAdminSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ['id', 'book', 'number', 'title', 'images']
        read_only_fields = ['id']

    def get_images(self, obj):
        image = Image.objects.filter(chapter=obj.id)
        return ImageSerializer(image, many=True).data


class ChapterViewSerializer(serializers.ModelSerializer):
    count_comments = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ['id', 'book', 'number', 'title', 'thumbnail', 'count_comments', 'date_modified',
                  'date_added', 'like_count', 'is_deleted']
        read_only_fields = ['id']

    def get_count_comments(self, obj):
        comment = Comment.objects.filter(chapter=obj).count()
        comment_ids = Comment.objects.filter(chapter=obj).values_list('id')
        reply = Reply.objects.filter(comment_id__in=comment_ids).count()

        return comment + reply


class ChapterDataSerializer(CustomModelSerializer):
    """
    ChapterDataSerializer
    """

    class Meta:
        model = Chapter
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['name_book'] = instance.book.title
        return response


class ExportChapterDataSerializer(CustomModelSerializer):
    """
    ExportChapterDataSerializer
    """

    class Meta:
        model = Chapter
        fields = ('id', 'title', 'book', 'number', 'thumbnail', 'like_count')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['name_book'] = instance.book.title
        return response


class ChapterDataCreateUpdateSerializer(CustomModelSerializer):
    """
    ChapterCreateSerializer
    """

    class Meta:
        model = Chapter
        fields = '__all__'


