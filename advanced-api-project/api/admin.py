"""
Admin configuration for the API application.

Register the Author and Book models so they appear in the Django
administration interface.  This makes it easy to inspect and
manually manage model instances while developing.
"""
from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publication_year', 'author')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author__name')
