from django.contrib import admin

from .models import Book
from author.models import Author


#
class AuthorInline(admin.TabularInline):
    model = Author.books.through


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'count', ('year_publication', 'relized_at')]
    list_display = ['id', 'name', 'count', 'year_publication', 'relized_at']
    search_fields = ['id', 'name', 'description', 'count', 'year_publication']
    list_display_links = ['id', 'name']
    list_filter = ('authors', 'id', 'name', 'year_publication')
    inlines = [AuthorInline]
    save_on_top = True