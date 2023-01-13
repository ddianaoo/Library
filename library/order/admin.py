from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display_links = ('id',)
    fields = ('book', 'user', ('plated_end_at', 'end_at'))
    list_display = ('id', 'book', 'user', 'plated_end_at', 'end_at')
    search_fields = ['book__name', 'user__email', 'user__first_name',
                     'user__last_name', 'user__middle_name']
    list_filter = ('book__name', 'user__email')
    save_on_top = True