"""
Django admin configuration for core app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models


class UserAdmin(BaseUserAdmin):
    """User admin configuration."""
    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name']
    # Add a new field to the list display for users
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        (
            'Permissions',
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        ('Important dates', {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']
    # Add a new fieldset for creating a new user
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),  # Custom CSS classes
                'fields': ('email',
                           'password1',
                           'password2',
                           'first_name',
                           'last_name',
                           'is_staff',
                           'is_superuser')
            }
        ),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Post)
admin.site.register(models.Tag)
