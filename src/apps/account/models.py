from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from core.models import TimestampedModel, SoftDeleteModel

from account import managers


class User(AbstractBaseUser, TimestampedModel, SoftDeleteModel):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    patronymic = models.CharField(max_length=100, blank=True, null=True)

    username = models.CharField(max_length=150, unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)

    # For Django Admin
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "email"]

    objects = managers.UserManager()

    def __str__(self):
        return f"{self.first_name} (@{self.get_username()})"

    def get_navigation_title(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def save(self, *args, **kwargs):
        from django.contrib.auth.hashers import make_password

        if self.password and not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)  # Hash the password

        return super().save(*args, **kwargs)
