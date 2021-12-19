import logging

from rest_framework import serializers

from apps.vadmin.op_drf.serializers import CustomModelSerializer
from books.models import Image, Comment
from books.serializers import ImageSerializer
from posts.models import PostGroup

from datetime import datetime
today = datetime.now()
today_path = today.strftime("%Y/%m/%d")

logger = logging.getLogger(__name__)


class PostGroupSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()

    class Meta:
        model = PostGroup
        fields = ['id', 'user', 'group', 'content', 'like_count', 'share_count',
                  'date_added', 'date_modified', 'is_deleted', 'image_url']

    # def get_image(self, obj):
    #     return ImageSerializer(Image.objects.filter(post=obj), many=True).data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = instance.user.name
        response['user_id'] = instance.user.id
        # response['avatar'] = instance.user.avatar
        response['group'] = instance.group.name
        response['group_id'] = instance.group.id
        try:
            response['avatar'] = instance.group.avatar.url
        except:
            response['avatar'] = ''
        comment = Comment.objects.filter(post_id=instance.id)
        response["comment_count"] = comment.count()

        return response


class PostGroupDataSerializer(CustomModelSerializer):
    """
    PostGroupDataSerializer
    """

    class Meta:
        model = PostGroup
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = instance.user.name
        response['group'] = instance.group.name
        return response


class ExportPostGroupDataSerializer(CustomModelSerializer):
    """
    ExportPostGroupDataSerializer
    """

    class Meta:
        model = PostGroup
        fields = '__all__'

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['name_book'] = instance.book.title
    #     return response


class PostGroupDataCreateUpdateSerializer(CustomModelSerializer):
    """
    PostGroupCreateSerializer
    """

    class Meta:
        model = PostGroup
        fields = '__all__'