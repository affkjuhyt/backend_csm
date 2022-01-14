import json
import logging

from rest_framework import serializers

from apps.vadmin.op_drf.serializers import CustomModelSerializer
from books.models import Comment, Reply, VulgarWord
from collector.models import Log
from userprofile.serializers import UserProfileSerializer
from apps.vadmin.permission.models import UserProfile

from django.utils import timezone

logger = logging.getLogger(__name__)


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'comment', 'user', 'reply', 'like_count', 'date_modified', 'date_added', 'is_deleted']
        read_only_fields = ['id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        reply = Reply.objects.filter(id=instance.id).first()
        response['user_name'] = reply.user.name
        try:
            response['avatar'] = reply.user.avatar.url
        except:
            response['avatar'] = ""
        response['user_id'] = reply.user.id
        response['level'] = reply.user.level

        return response


class CommentSerializer(serializers.ModelSerializer):
    # reply = ReplySerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'book', 'chapter', 'user', 'content', 'date_modified', 'date_added', 'like_count', 'is_deleted']
        read_only_fields = ['id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        replys = Reply.objects.filter(comment=instance)
        if replys.exists():
            response['user'] = replys.first().user.full_name
            response['level'] = replys.first().user.level
            response['time'] = timezone.now() - replys.first().date_added
            response['count_reply'] = replys.count()
            response['reply'] = ReplySerializer(replys, many=True).data
        else:
            response['user'] = ""
            response['level'] = ""
            response['time'] = ""
            response['count_reply'] = 0
            response['reply'] = ""

        return response


class CommentDataShowSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'book', 'chapter', 'user', 'content', 'reply', 'date_modified', 'date_added', 'like_count', 'is_deleted']
        read_only_fields = ['id']

    def get_reply(self, obj):
        list = []
        # return list.append(ReplySerializer(Reply.objects.filter(comment=obj).first()).data)
        data = ReplySerializer(Reply.objects.filter(comment=obj).first()).data
        list.append(data)
        return list

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['name'] = instance.user.name
        response['reply_count'] = Reply.objects.filter(comment=instance).count()
        try:
            response['avatar'] = instance.user.avatar.url
        except:
            response['avatar'] = ''
        # replys = Reply.objects.filter(comment=instance).first()
        # if replys.exists():
        #     response['user'] = replys.first().user.full_name
        #     response['level'] = replys.first().user.level
        #     response['time'] = timezone.now() - replys.first().date_added
        #     response['count_reply'] = replys.count()
        # else:
        #     response['user'] = ""
        #     response['level'] = ""
        #     response['time'] = ""
        #     response['count_reply'] = 0

        return response


class CommentDataSerializer(CustomModelSerializer):
    """
    CommentDataSerializer
    """

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['book'] = instance.book.title
        if not instance.chapter:
            response['chapter'] = ""
        else:
            response['chapter'] = instance.chapter.title
        response['user'] = instance.user.username
        log = Log.objects.filter(user_id=self.context['request'].id, event='like', type='comment', content_id=instance.id)
        if len(log) > 0:
            response['is_like'] = True
        else:
            response['is_like'] = False

        return response


class ExportCommentDataSerializer(CustomModelSerializer):
    """
    ExportCommentDataSerializer
    """

    class Meta:
        model = Comment
        fields = ('id', 'book', 'chapter', 'user', 'content', 'like_count')

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['name_book'] = instance.book.title
    #     return response


class CreateCommentDataSerializer(CustomModelSerializer):
    """
    ExportCommentDataSerializer
    """

    class Meta:
        model = Comment
        fields = ('id', 'book', 'chapter', 'user', 'content')


class CommentDataCreateUpdateSerializer(CustomModelSerializer):
    """
    CommentCreateSerializer
    """

    class Meta:
        model = Comment
        fields = '__all__'
