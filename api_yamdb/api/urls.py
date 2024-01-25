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
router_v1.register(r"categories", CategoriesViewSet, basename="categories")
router_v1.register(r"genres", GenresViewSet, basename="genres")
router_v1.register(r"titles", TitleViewSet, basename="titles")
router_v1.register(r"users", UsersViewSet, basename="users")

router_v1.register(
    r"^titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/auth/signup/", SignupView.as_view()),
    path(
        "v1/auth/token/",
        TokenObtainWithConfirmationView.as_view(),
        name="token_obtain_with_confirmation",
    ),
    path("v1/", include(router_v1.urls)),
]
