from rest_framework import serializers

from .models import Artisan


class ArtisanSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = Artisan
        fields = [
            "first_name",
            "last_name",
            "description",
            "birth_date",
            "services",
        ]
