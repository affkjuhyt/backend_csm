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
        exclude = ('creator', 'modifier')

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['name_book'] = instance.book.title
    #     return response


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

