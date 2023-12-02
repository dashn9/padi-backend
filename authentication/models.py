from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _


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
    COUNTRY_CHOICES = [
        ("NG", "Nigeria"),
    ]
    STATE_CHOICES = [
        ("AB", "Abia"),
        ("AD", "Adamawa"),
        ("AK", "Akwa Ibom"),
        ("AN", "Anambra"),
        ("BA", "Bauchi"),
        ("BE", "Benue"),
        ("BO", "Borno"),
        ("CR", "Cross River"),
        ("DE", "Delta"),
        ("EB", "Ebonyi"),
        ("ED", "Edo"),
        ("EK", "Ekiti"),
        ("EN", "Enugu"),
        ("FC", "Federal Capital Territory"),
        ("GO", "Gombe"),
        ("IM", "Imo"),
        ("JI", "Jigawa"),
        ("KA", "Kaduna"),
        ("KE", "Kano"),
        ("KO", "Kogi"),
        ("KW", "Kwara"),
        ("LG", "Lagos"),
        ("NA", "Nasarawa"),
        ("NI", "Niger"),
        ("OG", "Ogun"),
        ("ON", "Ondo"),
        ("OS", "Osun"),
        ("OY", "Oyo"),
        ("PL", "Plateau"),
        ("RI", "Rivers"),
        ("SO", "Sokoto"),
        ("TA", "Taraba"),
        ("YO", "Yobe"),
        ("ZA", "Zamfara"),
    ]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    username = None
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    birth_date = models.DateField(null=True, blank=True)
    state = models.CharField(
        max_length=2, choices=STATE_CHOICES, null=False, blank=False
    )
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default="NG")
    activated_at = models.DateTimeField(null=True, default=None)
    phone_number = models.CharField(max_length=50, blank=True)
    ip_addresses = ArrayField(models.GenericIPAddressField())

    objects = UserManager()

    class Meta:
        ordering = ["id"]


class UserGeolocation(models.Model):
    pass
