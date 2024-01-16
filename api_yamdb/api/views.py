from rest_framework import filters, permissions, viewsets, mixins

# from api.serializers import
from reviews.models import (
    Categories,
    Title,
    Genres,
    Users,
    Reviews,
    Comments
)


class CategoriesViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass


class GenresViewSet(viewsets.ModelViewSet):
    pass


class UsersViewSet(viewsets.ModelViewSet):
    pass


class ReviewsViewSet(viewsets.ModelViewSet):
    pass


class CommentsViewSet(viewsets.ModelViewSet):
    pass
