from rest_framework import serializers

from .models import Artisan, Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "service_code",
            "service_name",
            "service_group_name",
            "service_individual_name",
            "icon_name",
            "icon_color",
            "icon_back_drop_color",
        ]


class ServiceSerializerLight(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "service_code",
            "service_name",
            "service_group_name",
            "service_individual_name",
        ]


class ArtisanSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    birth_date = serializers.DateField(source="user.birth_date", read_only=True)
    joined = serializers.DateTimeField(
        source="created_at", read_only=True, format="%Y-%m-%d"
    )
    services = ServiceSerializerLight(many=True)

    class Meta:
        model = Artisan
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "bio",
            "birth_date",
            "joined",
            "services",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["state_full"] = instance.user.get_state_display()
        return representation


class ArtisanCreateSerializer(serializers.ModelSerializer):
    services = serializers.SlugRelatedField(
        slug_field="service_code",
        queryset=Service.objects.all(),
        many=True,
    )

    class Meta:
        model = Artisan
        fields = [
            "bio",
        ]


class ArtisanSerializerLight(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = Artisan
        fields = [
            "id",
            "first_name",
            "last_name",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["state_full"] = instance.user.get_state_display()
        return representation
