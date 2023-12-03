from rest_framework import serializers
from .models import EmailOtpAuthentication

class GenerateOtpForUserEmailVerificationSerializer(serializers.Serializer):
    # information required to process on successfull verification
    email = serializers.EmailField()

class GenerateOtpForUserSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=EmailOtpAuthentication.ACTIONS)
    verification_payload = serializers.DictField()

class VerifyOtpForUserEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=12)

class VerifyOtpForUserSerializer(serializers.Serializer):
    authenticator_id = serializers.IntegerField()
    otp = serializers.CharField(max_length=12)