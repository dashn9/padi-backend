from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .models import Artisan, Service
from .serializers import ArtisanSerializer, ArtisanSerializerLight, ServiceSerializer
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
        return [AllowAny()]

    @action(methods=["GET", "PUT"], detail=False)
    def me(self, request):
        (artisan, _) = Artisan.objects.get_or_create(user_id=request.user.id)
        if request.method == "GET":
            serializer = ArtisanSerializer(artisan)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = ArtisanSerializer(artisan, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

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
