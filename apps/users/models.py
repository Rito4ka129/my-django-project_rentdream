# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager, Group, Permission
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        }
    )
    first_name = models.CharField(
        _("first name"),
        max_length=40,
        validators=[MinLengthValidator(2)],
    )
    last_name = models.CharField(
        _("last name"),
        max_length=40,
        validators=[MinLengthValidator(2)],
    )
    email = models.EmailField(
        _("email address"),
        max_length=150,
        unique=True
    )
    # phone = models.CharField(max_length=75, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # date_joined = models.DateTimeField(name="registered", auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    # updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set', blank=True)
    is_landlord = models.BooleanField(default=False)
    tenant = models.BooleanField(default=False)

    ROLE_CHOICES = (
        ('landlord', 'landlord'),
        ('tenant', 'tenant'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
        # 'email',
        'role',
    ]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def is_authenticated(self):
        """Always return True. This is a required attribute for Django."""
        return True

    @property
    def is_anonymous(self):
        """Always return False. This is a required attribute for Django."""
        return False
