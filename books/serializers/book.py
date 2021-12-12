import logging

from rest_framework import serializers

from apps.vadmin.op_drf.serializers import CustomModelSerializer
from books.models import Book, TagBook, Tag, Chapter, Comment, Reply
from books.serializers.chapter import ChapterSerializer, ChapterAdminSerializer, ChapterViewSerializer
from userprofile.models import DownLoadBook, FollowBook

logger = logging.getLogger(__name__)


class BookSerializer(serializers.ModelSerializer):
    chapter = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'is_enable', 'thumbnail', 'description', 'author', 'date_modified',
                  'date_added', 'sex', 'status', 'type', 'like_count', 'view_count', 'star', 'is_vip', 'is_full', 'chapter']
        read_only_fields = ['id', 'is_enable']

    def get_chapter(self, obj):
        result = Chapter.objects.filter(book=obj)
        return ChapterViewSerializer(result, many=True).data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        chapter = Chapter.objects.filter(book=instance.id)
        tag_books = TagBook.objects.filter(book=instance.id)
        user = self.context.get('request').user
        if user.id == None:
            pass
        else:
            download = DownLoadBook.objects.filter(chapter__in=chapter).filter(user=user)
            count_chapter_download = download.count()
            response['count__chapter_download'] = count_chapter_download
        result = ""
        if tag_books.exists():
            for tag_book in tag_books:
                tag = Tag.objects.filter(id=tag_book.tag.id).first()
                result = result + str(tag.name) + ", "
            result_tag = result[:-2]
            response['tag'] = result_tag
        else:
            response['tag'] = ""

        if chapter.exists():
            response['count_chapter'] = chapter.count()
        else:
            response['count_chapter'] = 0

        comments = Comment.objects.filter(book_id=instance.id)
        comment_ids = comments.values_list('id')
        reply = Reply.objects.filter(comment__in=comment_ids)
        response['count_comment'] = comments.count() + reply.count()

        follow_book = FollowBook.objects.filter(book_id=instance.id)
        response['count_follow'] = follow_book.count()

        tag_books = TagBook.objects.filter(book=instance.id)
        result = ""
        if tag_books.exists():
            for tag_book in tag_books:
                tag = Tag.objects.filter(id=tag_book.tag.id).first()
                result = result + str(tag.name) + ", "
            result_tag = result[:-2]
            response['tag'] = result_tag
        else:
            response['tag'] = ""

        return response


class BookAdminSerializer(serializers.ModelSerializer):
    chapter = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['chapter']
        read_only_fields = ['id', 'is_enable']

    def get_chapter(self, obj):
        result = Chapter.objects.filter(book=obj).order_by('-date_added')
        return ChapterViewSerializer(result, many=True).data


class BookAdminViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'is_enable', 'thumbnail', 'description', 'author', 'date_modified',
                  'date_added', 'sex', 'status', 'type', 'like_count', 'view_count', 'star', 'is_vip', 'is_full']
        read_only_fields = ['id', 'is_enable']


class BookDataSerializer(CustomModelSerializer):
    """
    BookDataSerializer
    """

    class Meta:
        model = Book
        fields = '__all__'


class ExportBookDataSerializer(CustomModelSerializer):
    """
    ExportBookDataSerializer
    """

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'status', 'type', 'like_count', 'view_count', 'star', 'description')


class BookDataCreateUpdateSerializer(CustomModelSerializer):
    """
    BookCreateSerializer
    """

    class Meta:
        model = Book
        fields = '__all__'

