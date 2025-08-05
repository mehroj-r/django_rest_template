from django.db.models import ForeignObjectRel, QuerySet
from django.db.models.deletion import Collector


def SOFT_DELETE_CASCADE(
    collector: Collector, field: ForeignObjectRel, sub_objs: QuerySet, using: str
) -> None:
    """
    Custom CASCADE function that only marks objects for soft delete
    without recursive collection.

    Args:
        collector: The Django collector instance
        field: The field relationship being processed
        sub_objs: The QuerySet containing objects to process
        using: The database alias to use
    """
    if not hasattr(collector, "soft_deletes"):
        collector.soft_deletes = []

    collector.soft_deletes.extend(list(sub_objs))
