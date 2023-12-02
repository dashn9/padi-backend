from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .models import Artisan, Service
from .serializers import (
    ArtisanSerializer,
    ArtisanCreateSerializer,
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

    @action(methods=["GET", "PUT"], detail=False)
    def me(self, request):
        (artisan, _) = Artisan.objects.get_or_create(user_id=request.user.id)
        if request.method == "GET":
            serializer = ArtisanSerializer(artisan)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = ArtisanCreateSerializer(artisan, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

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
