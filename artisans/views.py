from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Artisan
from .serializers import ArtisanSerializer


class ArtisanProfileViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = ArtisanSerializer
    queryset = Artisan.objects.all()

    # One other way to acheive this will be to create a custom permission
    def get_permissions(self):
        # if self.request.method == "GET":
        #     return [AllowAny()]
        return [IsAuthenticated()]

    @action(methods=["GET", "PUT"], detail=False)
    def me(self, request):
        print(request.user)
        (artisan, _) = Artisan.objects.get_or_create(user_id=request.user.id)
        if request.method == "GET":
            serializer = ArtisanSerializer(artisan)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = ArtisanSerializer(artisan, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
