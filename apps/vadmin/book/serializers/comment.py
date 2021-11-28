from apps.vadmin.book.models import Comment
from apps.vadmin.op_drf.serializers import CustomModelSerializer

from datetime import datetime
today = datetime.now()
today_path = today.strftime("%Y/%m/%d")


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


class CommentDataCreateUpdateSerializer(CustomModelSerializer):
    """
    CommentCreateSerializer
    """

    class Meta:
        model = Comment
        fields = '__all__'

