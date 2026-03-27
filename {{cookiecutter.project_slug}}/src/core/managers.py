from django_softdelete.managers import (
    DeletedManager as DjangoDeletedManager,
    GlobalManager as DjangoGlobalManager,
    SoftDeleteManager as DjangoSoftDeleteManager,
)


class SoftDeleteManager(DjangoSoftDeleteManager):
    pass


class DeletedManager(DjangoDeletedManager):
    pass


class GlobalManager(DjangoGlobalManager):
    pass
