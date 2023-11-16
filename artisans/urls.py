from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register("services", views.ServiceViewSet)
router.register("", views.ArtisanProfileViewSet)

urlpatterns = router.urls
