from typing import Any

from django.contrib.admin import ModelAdmin
from django_softdelete.admin import (
    HARD_DELETE_ACTION,
    REGULAR_DELETE_ACTION_NAME,
    RESTORE_ACTION,
    SOFT_DELETE_ACTION,
)
from django_softdelete.filters import SoftDeleteFilter


class BaseModelAdmin(ModelAdmin):
    pass


class BaseSoftDeleteModelAdmin(BaseModelAdmin):
    def get_queryset(self, request) -> Any:
        return self.model.global_objects.get_queryset()

    def get_list_filter(self, request) -> Any:
        list_filter = super().get_list_filter(request) or []
        if not isinstance(list_filter, list):
            list_filter = list(list_filter)
        list_filter.append(SoftDeleteFilter)
        return list_filter

    def get_actions(self, request) -> Any:
        actions = super().get_actions(request)
        actions.pop(REGULAR_DELETE_ACTION_NAME, None)

        deleted_filter_value = {
            "true": True,
            "false": False,
            "all": "ALL",
        }[request.GET.get("is_deleted") or "all"]

        if deleted_filter_value is True:
            actions.update(RESTORE_ACTION)
            actions.update(HARD_DELETE_ACTION)
        elif deleted_filter_value is False or deleted_filter_value is None:
            actions.update(SOFT_DELETE_ACTION)
        elif deleted_filter_value == "ALL":
            actions.update(SOFT_DELETE_ACTION)
            actions.update(RESTORE_ACTION)
            actions.update(HARD_DELETE_ACTION)

        return actions
