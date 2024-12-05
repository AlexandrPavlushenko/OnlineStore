from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "username", "phone", "avatar", "country")
    search_fields = ("username", "email", "phone")
