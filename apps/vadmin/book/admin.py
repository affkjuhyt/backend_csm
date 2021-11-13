from django.contrib import admin

from apps.vadmin.book.models import Book
from apps.vadmin.book.models import Chapter


class BooksAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'description', 'type', 'status', 'is_vip', 'star', 'view_count',
        'like_count')
    search_fields = ['title', 'author']
    raw_id_fields = []
    list_filter = ['is_vip', 'status', 'is_enable']


class ChaptersAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'book', 'number', 'title', 'thumbnail', 'like_count'
    )
    search_fields = ['title']
    raw_id_fields = []
    list_filter = ['book']


admin.site.register(Book, BooksAdmin)
admin.site.register(Chapter, ChaptersAdmin)
