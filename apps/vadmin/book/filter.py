import django_filters

from apps.vadmin.book.models import Book
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
