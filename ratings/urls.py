from .views import RatingViewSet
from django.urls import path

# I created a custom url pattern here rather than using router, because I don't want anybody having direct access to the ratings
# Without a mandated filtering with the target_type and target_id
urlpatterns = [
    path(
        "<str:rating_target_type>/<int:rating_target_id>/",
        RatingViewSet.as_view({"get": "list"}),
        name="rating-list",
    ),
    path(
        "me/<str:rating_target_type>/<int:rating_target_id>/",
        RatingViewSet.as_view({"get": "me"}),
        name="my-rating",
    ),
    path(
        "aggregates/<str:rating_target_type>/<int:rating_target_id>/",
        RatingViewSet.as_view({"get": "aggregates"}),
        name="rating-aggregates",
    ),
    path("", RatingViewSet.as_view({"put": "create"}), name="rating-create"),
]
