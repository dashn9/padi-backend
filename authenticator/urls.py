from django.urls import path
from . import views

urlpatterns = [
    path(
        "otp/generate/",
        views.generate_otp,
        name="generate_otp",
    ),
    path(
        "otp/verify/",
        views.verify_otp,
        name="verify_otp",
    ),
]
