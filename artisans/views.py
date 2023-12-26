from django.db import transaction
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from .models import Artisan, Service
from .serializers import (
    ArtisanSerializer,
    ArtisanComposeSerializer,
    ArtisanSerializerLight,
    ServiceSerializer,
)
from .pagination import DefaultPagination
from .filters import ArtisanCustomFilter


class ArtisanProfileViewSet(ReadOnlyModelViewSet):
    serializer_class = ArtisanSerializer
    queryset = Artisan.objects.all()
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["user__first_name", "user__last_name"]
    filterset_class = ArtisanCustomFilter

    # One other way to acheive this will be to create a custom permission
    def get_permissions(self):
        return [IsAuthenticated()]

    # Figure out a better way to rewrite this me
    @action(methods=["GET", "PUT", "PATCH"], detail=False)
    @transaction.atomic
    def me(self, request):
        try:
            if request.method == "GET":
                artisan = Artisan.objects.get(user_id=request.user.id)
                serializer = ArtisanSerializer(artisan)
                return Response(serializer.data)
            elif request.method == "PUT":
                data = request.data
                data["user"] = request.user.id
                artisan, created = Artisan.objects.get_or_create(
                    user_id=request.user.id
                )
                serializer = ArtisanComposeSerializer(
                    instance=artisan, data=data, partial=not created
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        except Artisan.DoesNotExist:
            return Response(
                {"detail": "Artisan profile does not exist"}, status.HTTP_404_NOT_FOUND
            )

    @action(methods=["GET"], detail=False)
    def is_artisan(self, request):
        profile_count = Artisan.objects.filter(user_id=request.user.id).count()
        if profile_count == 1:
            return Response(True)
        return Response(False)

    def get_serializer_class(self):
        if self.action == "list":
            return ArtisanSerializerLight
        elif self.action == "retrieve":
            return ArtisanSerializer


class ServiceViewSet(ReadOnlyModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.filter(is_active=True).prefetch_related()
    lookup_field = "service_code"

    def get_permissions(self):
        return [IsAuthenticated()]
