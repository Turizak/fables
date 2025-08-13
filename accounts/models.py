import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

"""
When you use AbstractBaseUser, Django requires you to define a custom manager that knows how to create users and superusers.
- BaseUserManager gives you helper methods like normalize_email().
- create_user():
	- Validates required fields
	- Normalizes email
	- Calls set_password() to hash the password
- create_superuser():
	- Calls create_user() but also sets is_staff=True and is_superuser=True
Without this, createsuperuser command in Django would fail.
"""


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


"""
- AbstractBaseUser provides:
	- password field (securely hashed)
	- last_login field
	- set_password() and check_password() methods
- PermissionsMixin provides:
	- is_superuser field
	- Group and permission relationships
	- Methods like has_perm() and has_module_perms()
This means you no longer store passwords manually — Django handles hashing and verification.
- Email is now the primary login field (USERNAME_FIELD = "email").
- unique=True ensures no duplicate emails or usernames.
- username is still kept as a display name, but login is done via email.
"""


class Account(AbstractBaseUser, PermissionsMixin):
    index = models.AutoField(
        null=False,
        primary_key=True,
    )
    uuid = models.UUIDField(null=False, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(null=False, max_length=100, unique=True)
    email = models.EmailField(null=False, max_length=255, unique=True)
    last_updated = models.DateTimeField(null=False, auto_now=True)
    created_date = models.DateTimeField(null=False, auto_now_add=True)
    deleted = models.BooleanField(null=False, default=False)

    # Required for Django's admin and permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "email"  # Login with email
    REQUIRED_FIELDS = ["username"]  # Required when creating superuser

    class Meta:
        db_table = "account"

    def __str__(self):
        return self.username
