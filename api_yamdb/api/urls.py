from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoriesViewSet,
    CommentViewSet,
    GenresViewSet,
    ReviewViewSet,
    SignupView,
    TitleViewSet,
    TokenObtainWithConfirmationView,
    UsersViewSet,
)


router_v1 = DefaultRouter()
router_v1.register("categories", CategoriesViewSet, basename="categories")
router_v1.register("genres", GenresViewSet, basename="genres")
router_v1.register("titles", TitleViewSet, basename="titles")
router_v1.register("users", UsersViewSet, basename="users")

router_v1.register(
    r"^titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urls_v1_auth = urls_v1 = [
    path("signup/", SignupView.as_view()),
    path(
        "token/",
        TokenObtainWithConfirmationView.as_view(),
        name="token_obtain_with_confirmation",
    ),
]

urls_v1 = [
    path("", include(router_v1.urls)),
    path("auth/", include(urls_v1_auth)),
]

urlpatterns = [
    path("v1/", include(urls_v1)),
]
