from datetime import datetime

from rest_framework import serializers

from reviews.models import (
    Category,
    Title,
    Genre,
    Users,
    Reviews,
    Comments
)

YEAR_ERROR = 'Недействительный год выпуска!'


class CategoriesSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'

    class Meta:
        model = Category
        exclude = ('id',)


class GenresSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(YEAR_ERROR)
        return value


class UsersSerializer(serializers.ModelSerializer):
    pass


class ReviewsSerializer(serializers.ModelSerializer):
    pass


class CommentsSerializer(serializers.ModelSerializer):
    pass
