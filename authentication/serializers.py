from typing import Mapping

from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    else:
        return request.META.get("REMOTE_ADDR")


def update_user_ip(user, request):
    user.ip_addresses.append(get_client_ip(request))
    user.save(update_fields=["ip_addresses"])


class UserCreateSerializer(BaseUserCreateSerializer):
    is_full_name = True
    ip_address = serializers.ListField(
        source="ip_addresses", child=serializers.IPAddressField()
    )

    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "first_name",
            "last_name",
            "ip_address",
            "email",
            "phone_number",
            "password",
        ]

    def validate(self, data):
        if " " in data["first_name"]:
            raise serializers.ValidationError(
                {
                    "full_name"
                    if self.is_full_name
                    else "first_name": "First name cannot contain spaces."
                }
            )

        if " " in data["last_name"]:
            raise serializers.ValidationError(
                {
                    "full_name"
                    if self.is_full_name
                    else "last_name": "Last name cannnot contain spaces."
                }
            )
        return super().validate(data)

    def to_internal_value(self, data: Mapping):
        data["ip_address"] = [get_client_ip(self.context["request"])]
        # Seperate full_name(which is an optional value) into first_name and last_name if present
        if "full_name" in data:
            full_name_parts = data["full_name"].split(" ")
            if len(full_name_parts) >= 1:
                data["first_name"] = full_name_parts[0]
                data["last_name"] = " ".join(full_name_parts[1:])
        return super().to_internal_value(data)

    # I overrided this method so I could control the user data DRF CreateModelMixin returns after successfull User Registration
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {"first_name": data["first_name"], "email": data["email"]}


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        ## You can add more User model's attributes like username,email etc. in the data dictionary like this.
        update_user_ip(self.user, self.context["request"])
        return data


class GenerateOtpForUserSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOtpForUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=12)
