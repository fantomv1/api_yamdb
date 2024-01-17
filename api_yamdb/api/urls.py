from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    CategoriesViewSet,
    TitleViewSet,
    GenresViewSet,
    UsersViewSet,
    ReviewsViewSet,
    CommentsViewSet,
)


router = SimpleRouter() # # Временно для работы..

router.register("reviews", ReviewsViewSet, basename="reviews")  # Пример.

urlpatterns = [
    path("v1/", include(router.urls)),  # Временно для работы.
]
