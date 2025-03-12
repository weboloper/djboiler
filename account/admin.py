from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile

from django.db import models  # Import models to use field types like ManyToManyField

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

    # Optionally, you can customize the form here
    formfield_overrides = {
        models.ManyToManyField: {
            'widget': admin.widgets.FilteredSelectMultiple('Choices', is_stacked=False)
        },
        models.CharField: {
            'widget': admin.widgets.AdminRadioSelect
        }
    }

    # Optionally, specify the fields to display
    fields = ['avatar', 'bio',   'twitter', 'instagram', 'facebook', 'pinterest']


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('username',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username')
    ordering = ('email',)
    inlines = (ProfileInline,)
    readonly_fields = ["date_joined"]

# Register the User and Profile models
admin.site.register(User, UserAdmin)


 