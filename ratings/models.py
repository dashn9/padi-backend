from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class RatedItem(models.Model):
    rating_giver_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    rating_giver_id = models.PositiveIntegerField()
    rating_giver_object = GenericForeignKey()

    rating_target = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    rating_target_id = models.PositiveIntegerField()
    rating_target_object = GenericForeignKey()

    rating_comment = models.TextField()
    rating_stars_point = models.DecimalField(max_digits=2, decimal_places=1)
