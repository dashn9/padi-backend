from django.db import models
from django.conf import settings


# Icons on frontend are material community icons
class Service(models.Model):
    service_code = models.CharField(max_length=100, unique=True)
    service_name = models.CharField(max_length=100)

    service_group_name = models.CharField(max_length=100)

    icon_name = models.CharField(max_length=50)
    icon_color = models.CharField(max_length=7)
    icon_back_drop_color = models.CharField(max_length=7)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Artisan(models.Model):
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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField()
    birth_date = models.DateField()
    state = models.CharField(
        max_length=2, choices=STATE_CHOICES, null=False, blank=False
    )
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default="NG")
    services = models.ManyToManyField(Service)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
