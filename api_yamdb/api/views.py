from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.mixins import GetPostDeleteViewSet
from api.permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorModerAdminOrReadOnly,
)
from api.serializers import (
    CategoriesSerializer,
    CommentSerializer,
    GenresSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleSerializer,
    TokenObtainWithConfirmationSerializer,
    UserSerializer,
)
from api.utils import send_confirmation_email
from reviews.models import Category, Genre, Review, Title


User = get_user_model()


class CategoriesViewSet(GetPostDeleteViewSet):
    """Обрабатывает информацию о категориях."""

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(GetPostDeleteViewSet):
    """Обрабатывает информацию о жанрах."""

    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Обрабатывает информацию о произведениях."""

    serializer_class = TitleSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ("name",)
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    http_method_names = [
        m for m in viewsets.ModelViewSet.http_method_names if m not in ["put"]
    ]

    def get_queryset(self):
        """Добавить поле "rating" в queryset."""
        return Title.objects.annotate(rating=Avg("reviews__score")).order_by(
            "-year"
        )


class UsersViewSet(viewsets.ModelViewSet):
    """Создаёт новых пользователей."""

    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = "username"
    filter_backends = [filters.SearchFilter]
    search_fields = ["username"]
    http_method_names = [
        m for m in viewsets.ModelViewSet.http_method_names if m not in ["put"]
    ]

    def get_queryset(self):
        """Получить queryset."""
        return User.objects.all()

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def get_update_me(self, request):
        """Получить и обновить информацию о текущем пользователе."""
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=self.request.user.role)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class TokenObtainWithConfirmationView(CreateAPIView):
    """Создаёт токен по запросу пользователя."""

    serializer_class = TokenObtainWithConfirmationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """Создать токен."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data["username"]
        )
        if default_token_generator.check_token(
            user, serializer.validated_data["confirmation_code"]
        ):
            token = AccessToken.for_user(user)
            return Response(
                {"token": str(token)},
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    """Регистрирует нового пользователя."""

    def post(self, request, *args, **kwargs):
        """Проверить и зарегистрировать нового пользователя."""

        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)

        # Отправить письмо с кодом.
        confirmation_code = send_confirmation_email(user.email)
        default_token_generator.check_token(user, confirmation_code)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """Обрабатывает информацию об отзывах."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModerAdminOrReadOnly,
    )
    http_method_names = [
        m for m in viewsets.ModelViewSet.http_method_names if m not in ["put"]
    ]

    def get_title(self):
        """Получить произведение."""
        title = self.kwargs.get("title_id")
        return get_object_or_404(Title, id=title)

    def get_queryset(self):
        """Вернуть все отзывы к произведению."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Добавить автора отзыва и id произведения."""
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Обрабатывает информацию о комментариях."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModerAdminOrReadOnly,
    )
    http_method_names = [
        m for m in viewsets.ModelViewSet.http_method_names if m not in ["put"]
    ]

    def get_review(self):
        """Получить отзыв."""
        return get_object_or_404(Review, id=self.kwargs.get("review_id"))

    def get_queryset(self):
        """Вернуть все комментарии к отзыву."""
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        """Добавить автора комментария и id отзыва."""
        serializer.save(author=self.request.user, review=self.get_review())
