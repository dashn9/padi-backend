from django.db import models
from django.conf import settings


# Icons on frontend are material community icons
class Service(models.Model):
    service_code = models.CharField(max_length=100, unique=True)
    service_name = models.CharField(max_length=100)

    service_group_name = models.CharField(max_length=100)
    service_individual_name = models.CharField(max_length=100)

    icon_name = models.CharField(max_length=50)
    icon_color = models.CharField(max_length=7)
    icon_back_drop_color = models.CharField(max_length=7)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Artisan(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField()
    # rename to ArtisanServices for more clarity
    services = models.ManyToManyField(Service, through="ArtisanService")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Rename to ArtisanServices for more clarity, but be care full, do it when you are about to run a clean migration to the db
# Also run the Artisan Services seeder command to reset table id before populating to prevent issues.
class ArtisanService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    artisan = models.ForeignKey(Artisan, on_delete=models.DO_NOTHING)
