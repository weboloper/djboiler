from django.contrib import admin
from .models import User, Profile
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class MyUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    readonly_fields = ["date_joined"]
    # Optionally, add the custom field to the fieldsets (if you want it to appear in a specific section)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('email_verified',)}),  # Add custom field to the fieldset
    )

admin.site.register(User,MyUserAdmin)