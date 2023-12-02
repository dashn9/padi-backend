from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Rating(models.Model):
    rating_giver = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True
    )

    rating_target_id = models.BigIntegerField()

    # Use a settings configuration choice fields to limit the possibilities of the types
    rating_target_type = models.CharField(max_length=100)

    rating_comment = models.TextField()
    rating_stars_point = models.DecimalField(max_digits=2, decimal_places=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
