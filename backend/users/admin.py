from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'surname', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    ordering = ('-id',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'avatar', 'phone', 'github_url', 'about')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'surname', 'phone', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    
    search_fields = ('email', 'name', 'surname')
