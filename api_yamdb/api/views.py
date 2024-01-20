from rest_framework import filters, permissions, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions

from django.core.mail import send_mail
from django.conf import settings


from reviews.models import Category, Title, Genre, User, Reviews, Comments
from api.serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitleSerializer,
    UsersSerializer,
    TokenObtainWithConfirmationSerializer,
    UserProfileSerializer,
    ReviewsSerializer,
    CommentsSerializer,
)
from api.utils import send_confirmation_email


class CategoriesViewSet(viewsets.ModelViewSet):
    """Обрабатывает информацию о категориях."""

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(viewsets.ModelViewSet):
    """Обрабатывает информацию о жанрах."""

    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Обрабатывает информацию о произведениях."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class UsersViewSet(viewsets.ModelViewSet):
    """Обрабатывает информацию о юзерах."""

    queryset = User.objects.all()
    serializer_class = UsersSerializer


class UserProfileUpdateView(generics.UpdateAPIView):
    """пользователь отправляет PATCH-запрос на эндпоинт
    /api/v1/users/me/ и заполняет поля в своём профайле."""

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class TokenObtainWithConfirmationView(TokenObtainPairView):
    """Пользователь отправляет пост запрос,
    и в ответ получает токен."""

    serializer_class = TokenObtainWithConfirmationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']

        if username == 'valid_username' and confirmation_code == 'valid_code':
            return super().post(request, *args, **kwargs)
        else:
            return Response(
                {'error': 'Invalid username or confirmation code'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SignupView(APIView):
    """Класс добавления нового пользователя и
       отправки письма с кодом на почту."""

    def post(self, request, *args, **kwargs):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Вызов вашей функции для отправки письма с кодом
            confirmation_code = send_confirmation_email(user.email)

            # Возвращение ответа с данными пользователя и кодом подтверждения
            response_data = {
                'user': serializer.data,
                'confirmation_code': confirmation_code,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewsViewSet(viewsets.ModelViewSet):
    pass


class CommentsViewSet(viewsets.ModelViewSet):
    pass
