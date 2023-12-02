from rest_framework import serializers


class GenerateOtpForUserSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOtpForUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=12)
