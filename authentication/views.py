from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import EmailOtpForVerification
from .serializers import (
    get_client_ip,
    GenerateOtpForUserSerializer,
    VerifyOtpForUserSerializer,
)


def check_email_verifiable(email):
    try:
        if get_user_model().objects.get(email=email).is_active:
            return Response(
                {"detail": "You can't generate/verify an OTP for this email"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except get_user_model().DoesNotExist:
        return Response(
            {"detail": "You can't generate/verify an OTP for this email"},
            status=status.HTTP_404_NOT_FOUND,
        )
    return True


@api_view(["PUT"])
def generate_otp_for_email_activation(request: Request):
    generate_otp_serializer = GenerateOtpForUserSerializer(data=request.data)
    if not generate_otp_serializer.is_valid():
        return Response(
            generate_otp_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    email = generate_otp_serializer.data["email"]
    # Get the client's IP address from the request
    client_ip = get_client_ip(request)
    print(client_ip)
    email_verifiable = check_email_verifiable(email)
    if not email_verifiable == True:
        return email_verifiable

    otp_instance, _ = EmailOtpForVerification.objects.get_or_create(email=email)

    if otp_instance.is_verified:
        return Response(
            {"detail": "Email already verified"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Update the number of generation tries and IP addresses
    otp_instance.no_of_generation_tries += 1
    otp_instance.ip_addresses.append(client_ip)
    otp_instance.gen_otp()
    otp_instance.save()

    subject = "Your OTP Code"
    message = f"Your OTP code is: {otp_instance.otp}"
    from_email = "your_email@gmail.com"  # The sender's email address
    recipient_list = [email]  # Recipient's email address

    send_mail(subject, message, from_email, recipient_list)

    return Response(
        {"detail": "OTP created successfully"}, status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
def verify_otp_for_email_activation(request: Request):
    generate_otp_serializer = VerifyOtpForUserSerializer(data=request.data)
    if not generate_otp_serializer.is_valid():
        return Response(
            generate_otp_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    email, otp = generate_otp_serializer.data.values()
    print(email, otp)
    # Get the client's IP address from the request
    client_ip = get_client_ip(request)

    email_verifiable = check_email_verifiable(email)

    if not email_verifiable == True:
        return email_verifiable

    try:
        otp_instance = EmailOtpForVerification.objects.get(email=email)
    except EmailOtpForVerification.DoesNotExist:
        return Response(
            {"detail": "You can't verify an OTP for this email"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Update the number of verification tries and IP addresses
    otp_instance.no_of_verification_tries += 1
    otp_instance.ip_addresses.append(client_ip)
    otp_instance.save()

    # Once you are done, seperate some stuffs like the OTP_EXPIRATION_TIME into the settings file
    expiration_time = timezone.now() - timezone.timedelta(minutes=30)
    if otp_instance.updated_at < expiration_time:
        return Response({"detail": "OTP has expired"}, status=status.HTTP_403_FORBIDDEN)

    if otp_instance.is_verified:
        return Response(
            {"detail": "Email already verified"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Check OTP expiration
    expiration_time = timezone.now() - timezone.timedelta(
        minutes=30
    )  # Adjust as needed
    if otp_instance.updated_at < expiration_time:
        return Response(
            {"detail": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
        )

    if otp_instance.otp == otp:
        otp_instance.is_verified = True
        user = get_user_model().objects.filter(email=email)
        user.update(is_active=True, activated_at=timezone.now())
        otp_instance.save()
        return Response(
            {"detail": "Email successfully verified"}, status=status.HTTP_200_OK
        )
    else:
        return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
