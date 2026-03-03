from django.contrib import admin

from account.models import User
from core.admin import BaseModelAdmin


@admin.register(User)
class UserAdmin(BaseModelAdmin):
    list_display = ("id", "phone", "first_name", "last_name", "patronymic", "is_active")
    search_fields = ("phone", "first_name", "last_name", "patronymic")
    ordering = ("-created_at",)
    exclude = ("last_login", "deleted_at")
    list_display_links = ("id", "phone")
