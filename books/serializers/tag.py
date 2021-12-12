import logging

from rest_framework import serializers

from books.models import Tag, TagBook, Book
from books.serializers.book import BookAdminSerializer, BookAdminViewSerializer

logger = logging.getLogger(__name__)


class TagSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'date_modified', 'book', 'date_added', 'is_deleted']
        read_only_fields = ['id']

    def get_book(self, obj):
        tag_book_ids = TagBook.objects.filter(tag__name=obj.name).values_list('book')
        books = Book.objects.filter(pk__in=tag_book_ids)

        return BookAdminViewSerializer(books, many=True).data


class TagBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagBook
        fields = ['id', 'tag', 'book', 'date_modified', 'date_added', 'is_deleted']
        read_only_fields = ['id']

