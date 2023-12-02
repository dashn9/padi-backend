from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import RatingSerializer
from .models import Rating


class RatingViewSet(ListCreateAPIView, GenericViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.filter(deleted_at=None)
    lookup_field = "rating_target_type__rating_target_id"

    def get_permissions(self):
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        self.request.data["rating_giver"] = self.request.user.id
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return Rating.objects.filter(
            deleted_at=None,
            rating_target_type=self.kwargs.get("rating_target_type"),
            rating_target_id=self.kwargs.get("rating_target_id"),
        )
