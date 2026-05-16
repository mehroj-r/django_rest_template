from django_softdelete.managers import DeletedManager as DjangoDeletedManager
from django_softdelete.managers import GlobalManager as DjangoGlobalManager
from django_softdelete.managers import SoftDeleteManager as DjangoSoftDeleteManager


class SoftDeleteManager(DjangoSoftDeleteManager):
    pass


class DeletedManager(DjangoDeletedManager):
    pass


class GlobalManager(DjangoGlobalManager):
    pass
