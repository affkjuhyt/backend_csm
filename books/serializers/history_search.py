import logging

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework import serializers

from books.models import HistorySearch, Book, TagBook, Tag

logger = logging.getLogger(__name__)


class HistorySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorySearch
        fields = ['id', 'user', 'text', 'date_modified', 'date_added', 'is_deleted']
        read_only_fields = ['id']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        text = instance.text
        search_vectors = SearchVector('title', weight='A') + SearchVector('author', weight='B') + SearchVector(
            'type', weight='C') + SearchVector('description', weight='D')

        search_query = SearchQuery(text)
        search_rank = SearchRank(search_vectors, search_query)
        book_ids = Book.objects.annotate(
            rank=search_rank
        ).order_by('-rank').values_list('id')
        tag_book_ids = TagBook.objects.filter(book_id__in=book_ids).values_list('tag_id').distinct()
        tag = Tag.objects.filter(pk__in=tag_book_ids).order_by('?').first()
        response['tag'] = tag.name

        return response
