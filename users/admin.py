from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class MyUserAdmin(UserAdmin):
    readonly_fields = ["date_joined"]

admin.site.register(User,MyUserAdmin)