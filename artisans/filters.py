from django_filters.rest_framework import FilterSet
from .models import Artisan


class ArtisanCustomFilter(FilterSet):
    class Meta:
        model = Artisan
        fields = {"services__service_code": ["in"], "user__state": ["exact"]}
