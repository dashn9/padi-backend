from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone

# Create your models here.


class EmailOtpAuthentication(models.Model):
    ACTIONS = [("verify_email", "V-E")]

    email = models.EmailField()
    otp = models.CharField(max_length=12)
    no_of_generation_tries = models.IntegerField(default=0)
    no_of_verification_tries = models.IntegerField(default=0)
    action = models.CharField(choices=ACTIONS, null=False, blank=False)
    payload = models.JSONField(default=dict)
    used = models.BooleanField(default=False)
    ip_addresses = ArrayField(models.GenericIPAddressField(), default=list)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(null=True, blank=True)

    def gen_otp(self):
        self.otp = get_random_string(length=6, allowed_chars="0123456789")

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(EmailOtpAuthentication, self).save(*args, **kwargs)
