from rest_framework import serializers

from reviews.models import (
    Categories,
    Title,
    Genres,
    Users,
    Reviews,
    Comments
)


class CategoriesSerializer(serializers.ModelSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    pass


class GenresSerializer(serializers.ModelSerializer):
    pass


class UsersSerializer(serializers.ModelSerializer):
    pass


class ReviewsSerializer(serializers.ModelSerializer):
    pass


class CommentsSerializer(serializers.ModelSerializer):
    pass
