from django.contrib.auth import get_user_model
from django.core.exceptions import SuspiciousOperation
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class ValidateMixin:
    def validate(self, data):
        if User.objects.filter(
            username=data.get('username'), email=data.get('email')
        ).exists():
            return data
        elif User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError('Это имя уже занято')
        elif User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError('Эта почта уже занята')
        return data

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Вы не можете использовать это имя'
            )
        return value


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ("id",)


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ("id",)


class CategoriesTitle(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategoriesSerializer(value)
        return serializer.data


class GenresTitle(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenresSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoriesTitle(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = GenresTitle(
        slug_field="slug", queryset=Genre.objects.all(), many=True,
        allow_empty=False, required=True
    )

    class Meta:
        model = Title
        fields = "__all__"


class GetTitleSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = "__all__"


class SignUpSerializer(ValidateMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )

    def validate_username(self, value):
        if value.lower() == "me":
            raise ValidationError('Недопустимое значение "me" для username')
        return value    


class TokenObtainWithConfirmationSerializer(ValidateMixin, serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate_username(self, value):
        if value.lower() == "me":
            raise ValidationError('Недопустимое значение "me" для username')
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        model = Review
        exclude = ("title",)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        model = Comment
        exclude = ("review_id",)
