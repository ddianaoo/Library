from django.contrib import admin
from .forms import *
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_form = UserRegisterForm
    model = CustomUser
    list_display = ('id', 'email', 'role', 'is_superuser', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active', 'role', 'is_superuser',)
    fieldsets = ((None, {'fields': ('email', 'role')}),
                 ("Personal info", {'classes': ('wide',),
                                    "fields": ('first_name', 'last_name', 'middle_name',)}),
                 ('Permissions', {'classes': ('wide',),
                                  'fields': ('is_staff', 'is_superuser', 'is_active')}))
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_active', 'is_superuser')}
         ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'middle_name')
    ordering = ('-id',)
    list_editable = ['is_active']
    list_display_links = ('id', 'email')
    save_on_top = True


admin.site.register(CustomUser, CustomUserAdmin)
