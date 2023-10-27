from django.db import models
from django.conf import settings


class Services(models.Model):
    service_code = models.CharField(max_length=100)
    service_name = models.CharField(max_length=100)


class Artisan(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    birth_date = models.DateField()
    services = models.ManyToManyField(Services)
