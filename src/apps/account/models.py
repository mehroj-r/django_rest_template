from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimestampedModel, SoftDeleteModel
from django.contrib.auth.hashers import make_password

from apps.account import managers


class User(AbstractBaseUser, TimestampedModel, SoftDeleteModel):

    first_name = models.CharField(max_length=30, verbose_name=_("First Name"))
    last_name = models.CharField(
        max_length=30, verbose_name=_("Last Name"), blank=True, null=True
    )
    patronymic = models.CharField(
        max_length=100, verbose_name=_("Patronymic"), blank=True, null=True
    )

    username = models.CharField(max_length=150, unique=True, verbose_name=_("Username"))
    phone = models.CharField(
        max_length=15,
        unique=True,
        verbose_name=_("Phone Number"),
        null=True,
        blank=True,
    )
    email = models.EmailField(unique=True, verbose_name=_("Email"))

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "email"]

    # For Django Admin
    is_staff = models.BooleanField(default=False, verbose_name=_("Is staff"))
    is_superuser = models.BooleanField(default=False, verbose_name=_("Is superuser"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    objects = managers.UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.first_name} (@{self.get_username()})"

    def get_navigation_title(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def save(self, *args, **kwargs):

        if self.password and not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)  # Hash the password

        return super().save(*args, **kwargs)
