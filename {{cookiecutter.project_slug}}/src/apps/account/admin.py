from account.models import User
from core.admin import BaseSoftDeleteModelAdmin
from django.contrib import admin


@admin.register(User)
class UserAdmin(BaseSoftDeleteModelAdmin):
    list_display = (
        "id",
        "phone",
        "first_name",
        "last_name",
        "patronymic",
        "is_active",
        "is_deleted",
    )
    search_fields = ("phone", "first_name", "last_name", "patronymic")
    list_filter = ("is_active",)
    ordering = ("-created_at",)
    exclude = ("last_login", "deleted_at", "restored_at", "transaction_id")
    list_display_links = ("id", "phone")
