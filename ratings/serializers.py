from django.contrib.auth import get_user_model

from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    rating_giver = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.filter(is_active=True), write_only=True
    )
    rating_giver_first_name = serializers.CharField(
        source="rating_giver.first_name", read_only=True
    )

    rating_giver_last_name = serializers.CharField(
        source="rating_giver.last_name", read_only=True
    )
    rating_stars_point = serializers.DecimalField(
        max_value=5, min_value=1, max_digits=2, decimal_places=1
    )

    class Meta:
        model = Rating
        fields = [
            "rating_giver",
            "rating_giver_first_name",
            "rating_giver_last_name",
            "rating_target_id",
            "rating_target_type",
            "rating_comment",
            "rating_stars_point",
        ]
