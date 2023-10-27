from django.urls import path
from . import views

urlpatterns = [
    path(
        "otp/generate/user-activation",
        views.generate_otp_for_email_activation,
        name="generate_otp_for_email_activation",
    ),
    path(
        "otp/verify/user-activation",
        views.generate_otp_for_email_activation,
        name="verify_otp_for_email_activation",
    ),
]
