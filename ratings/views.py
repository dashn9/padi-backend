from django.db.models import Avg

from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import RatingSerializer
from .models import Rating
from .pagination import DefaultPagination


class RatingViewSet(ListCreateAPIView, GenericViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.filter(deleted_at=None)
    lookup_field = "rating_target_type__rating_target_id"
    pagination_class = DefaultPagination

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

    @action(methods=["GET"], detail=False)
    def aggregates(self, request, *args, **kwargs):
        if request.method == "GET":
            queryset = self.get_queryset()
            ratings_average = queryset.aggregate(Avg("rating_stars_point"))[
                "rating_stars_point__avg"
            ]
            ratings_count = queryset.count()
            return Response(
                {
                    "rating_stars_average": round(ratings_average or 0, 2),
                    "ratings_count": ratings_count,
                }
            )

    @action(methods=["GET"], detail=False)
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            try:
                queryset = self.get_queryset()
                my_rating = queryset.filter(rating_giver=request.user)
                return Response(self.get_serializer(my_rating.get()).data)
            except Rating.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
