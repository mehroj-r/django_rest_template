from django.contrib.auth.base_user import BaseUserManager
from django_softdelete.managers import SoftDeleteManager, SoftDeleteQuerySet


class UserQuerySet(SoftDeleteQuerySet):
    pass


class UserManager(SoftDeleteManager, BaseUserManager):
    use_in_migrations = True

    def get_queryset(self):
        base_queryset = super().get_queryset()
        return UserQuerySet(model=self.model, query=base_queryset.query, using=self._db)

    def get_by_natural_key(self, username):
        """Returns the user by their username field."""
        return self.get(**{self.model.USERNAME_FIELD: username})

    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and returns a user with given username, password.
        """
        if not username:
            raise ValueError(f"The username field must be set: {self.model.USERNAME_FIELD}")

        email = extra_fields.get("email")
        if email:
            extra_fields["email"] = self.normalize_email(email)

        user = self.model(**{self.model.USERNAME_FIELD: username}, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Creates and returns a superuser with username and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, password, **extra_fields)
