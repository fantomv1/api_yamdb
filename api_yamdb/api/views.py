from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets, mixins

from reviews.models import (
    Category,
    Title,
    Genre,
    Users,
    Review,
    Comment,
    User_test
)
from api.serializers import (
    CategoriesSerializer, GenresSerializer, TitleSerializer,
    UsersSerializer, ReviewSerializer, CommentSerializer
)
from api.import_csv import import_base


def test():  # Костыль для работы баз данных
    # import_base(model=Category, file="D:/Dev/api_yamdb/api_yamdb/static/data/category.csv")
    # import_base(model=Genre, file="D:/Dev/api_yamdb/api_yamdb/static/data/genre.csv")
    # import_base(model=Title, file="D:/Dev/api_yamdb/api_yamdb/static/data/titles.csv")
    # import_base(model=User_test, file="D:/Dev/api_yamdb/api_yamdb/static/data/users.csv")
    import_base(model=Review, file="D:/Dev/api_yamdb/api_yamdb/static/data/review.csv")
    # import_base(model=Comment, file="D:/Dev/api_yamdb/api_yamdb/static/data/comments.csv")


#test()


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
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    """Обрабатывает информацию об отзывах."""

    serializer_class = ReviewSerializer
    permission_classes = (
        # IsAuthorOrReadOnly,
        # permissions.IsAuthenticatedOrReadOnly,
    )

    def get_title(self):
        """Получить произведение."""
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        """Вернуть все отзывы к произведению."""
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        """Добавить автора отзыва и id произведения."""
        serializer.save(
            author=None,  # author=self.request.user,
            title_id=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Обрабатывает информацию о комментариях."""

    serializer_class = CommentSerializer
    permission_classes = (
        # IsAuthorOrReadOnly,
        # permissions.IsAuthenticatedOrReadOnly,
    )

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
        serializer.save(
            author=None,  # author=self.request.user,
            review_id=self.get_review()
        )
