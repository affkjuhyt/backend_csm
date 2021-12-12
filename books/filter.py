import django_filters

from books.models import Book, Chapter, Image, Comment
from django.db import models


class BookDataFilter(django_filters.rest_framework.FilterSet):
    """
    Phan bo du lieu
    """
    title = django_filters.CharFilter(lookup_expr='icontains')
    type = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Book
        exclude = ('thumbnail',)


class ChapterDataFilter(django_filters.rest_framework.FilterSet):
    """
    Phan loai du lieu
    """

    title = django_filters.CharFilter(lookup_expr='icontains')
    # book = django_filters.CharFilter(field_name='book__title', lookup_expr='iexact')

    class Meta:
        models = Chapter
        exclude = ('thumbnail',)


class SaveImageFilter(django_filters.rest_framework.FilterSet):
    """
    文件管理 简单过滤器
    """
    # name = django_filters.CharFilter(lookup_expr='icontains')
    chapter = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Image
        exclude = ('image',)


class CommentFilter(django_filters.rest_framework.FilterSet):
    """
    Filter comment
    """
    # book = django_filters.CharFilter(lookup_expr='icontains')
    # chapter = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Comment
        fields = '__all__'
