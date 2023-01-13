from django.contrib import admin

from .models import Author
from book.models import Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['name', 'surname', 'patronymic', 'books', ('date_of_birth', 'date_of_death')]
    list_display = ['id', 'name', 'surname', 'patronymic']
    list_display_links = ('id', 'name', 'surname', 'patronymic')
    # filter_horizontal = ('books',)
    search_fields = ['id', 'name', 'surname', 'patronymic', 'books__name']
    list_filter = ['name', 'surname', 'patronymic', 'books__name']
    save_on_top = True
