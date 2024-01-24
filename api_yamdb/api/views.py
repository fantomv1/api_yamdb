from django.contrib.auth import get_user_model
from django.core.exceptions import SuspiciousOperation
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny,
)
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView

from reviews.models import Category, Title, Genre, Review
from api.serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitleSerializer,
    GetTitleSerializer,
    SignUpSerializer,
    TokenObtainWithConfirmationSerializer,
    UserSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from api.permissions import (
    IsAdminOrReadOnly,
    IsAuthorModerAdminOrReadOnly,
    IsAdmin,
)
from api.filters import TitleFilter
from api.utils import send_confirmation_email


User = get_user_model()


class GetPostDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoriesViewSet(GetPostDeleteViewSet):
    """Обрабатывает информацию о категориях."""

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class GenresViewSet(GetPostDeleteViewSet):
    """Обрабатывает информацию о жанрах."""

    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Обрабатывает информацию о произведениях."""

    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter
    http_method_names = [
        m for m in viewsets.ModelViewSet.http_method_names if m not in ['put']
    ]

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg("reviews__score")
        ).order_by("-year")

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return GetTitleSerializer
        return TitleSerializer


class UsersViewSet(viewsets.ModelViewSet):  # ВЬЮСЕТ НА ПРОСМОТР И ДОБАВЛЕНИЕ
    """Обрабатывает информацию о юзерах."""

    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'


class UserProfileUpdateView(RetrieveUpdateAPIView):
    """Пользователь отправляет PATCH-запрос на эндпоинт
    /api/v1/users/me/ и заполняет поля в своём профайле."""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class TokenObtainWithConfirmationView(CreateAPIView):
    """Пользователь отправляет пост запрос,
    и в ответ получает токен."""

    serializer_class = TokenObtainWithConfirmationSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']

        if username == "me":
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username)

        if confirmation_code == user.confirmation_code:
            token = AccessToken.for_user(user)
            return Response(
                {"token": str(token)},
                status=status.HTTP_200_OK,
            )

        return Response(status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    """Регистрирует нового пользователя."""

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)

        # Проверка, если значение поля username равно "me"
        if username == "me":
            return Response(
                {'detail': 'Недопустимое значение "me" для username'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, существует ли пользователь с таким именем пользователя
        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            return Response(
                {'detail': 'Пользователь уже зарегистрирован'},
                status=status.HTTP_200_OK
            )

        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Отправить письмо с кодом.
            confirmation_code = send_confirmation_email(user.email)

            user.confirmation_code = confirmation_code
            user.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        errors = serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    """Обрабатывает информацию об отзывах."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModerAdminOrReadOnly,
    )
    http_method_names = [
        m for m in viewsets.ModelViewSet.http_method_names if m not in ['put']
    ]

    def get_title(self):
        """Получить произведение."""
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        """Вернуть все отзывы к произведению."""
        title = self.get_title()
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        """Добавить автора отзыва и id произведения."""
        title_id = self.kwargs.get("title_id")
        if Review.objects.filter(
            title_id=title_id,
            author=self.request.user
        ).exists():
            raise SuspiciousOperation('Invalid JSON')
        serializer.save(
            author=self.request.user,
            title_id=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Обрабатывает информацию о комментариях."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModerAdminOrReadOnly,
    )
    http_method_names = [
        m for m in viewsets.ModelViewSet.http_method_names if m not in ['put']
    ]

    def get_review(self):
        """Получить отзыв."""
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        """Вернуть все комментарии к отзыву."""
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        """Добавить автора комментария и id отзыва."""
        serializer.save(author=self.request.user, review_id=self.get_review())
