import logging

from rest_framework import serializers

from bookcase.models import History
from books.models import Book, Chapter

logger = logging.getLogger(__name__)


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'user', 'book', 'chapter', 'hide']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        book = Book.objects.filter(id=instance.book.id).first()
        response["chapter_read"] = instance.chapter.number
        response["book_name"] = book.title
        chapter = Chapter.objects.filter(book_id=book.id).last()
        response["chapter_last"] = chapter.number

        return response

