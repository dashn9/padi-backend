from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from django.utils.crypto import get_random_string
from django.utils import timezone


# Add a logout endpoint to My.Padi, this is a todo
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class UserImage(models.Model):
    user_id = models.BigIntegerField(null=False, blank=False)
    image_location = models.CharField(max_length=255)
    image = models.ImageField(upload_to=f"images/{user_id}/")
    created_at = models.DateTimeField(auto_now_add=True)


# Create a celery task that automatically resolves inactive users to another db and deletes them from the main auth db
class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    username = None
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    activated_at = models.DateTimeField(null=True, default=None)
    phone_number = models.CharField(max_length=50, blank=True)
    ip_addresses = ArrayField(models.GenericIPAddressField())

    objects = UserManager()

    class Meta:
        ordering = ["id"]


class EmailOtpForVerification(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=12)
    no_of_generation_tries = models.IntegerField(default=0)
    no_of_verification_tries = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    ip_addresses = ArrayField(models.GenericIPAddressField(), default=list)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(null=True, blank=True)

    def gen_otp(self):
        self.otp = get_random_string(length=6, allowed_chars="0123456789")

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(EmailOtpForVerification, self).save(*args, **kwargs)
