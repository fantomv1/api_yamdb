from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.numbers import (
    DEFAULT_NUM,
    MAX_LEN_EMAIL,
    MAX_LEN_USERNAME
)
from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False,
        required=True,
    )
    rating = serializers.IntegerField(read_only=True, default=DEFAULT_NUM)

    class Meta:
        model = Title
        fields = "__all__"

    def to_representation(self, instance):
        representation = super(
            TitleSerializer, self
        ).to_representation(instance)
        representation['genre'] = CategoriesSerializer(
            instance.genre.all(), many=True
        ).data
        if instance.category:
            representation['category'] = GenresSerializer(
                instance.category
            ).data
        return representation


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+\Z", max_length=MAX_LEN_USERNAME
    )
    email = serializers.EmailField(max_length=MAX_LEN_EMAIL)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )

    def validate(self, data):
        if User.objects.filter(
            username=data.get("username"), email=data.get("email")
        ).exists():
            return data
        if User.objects.filter(username=data.get("username")).exists():
            raise serializers.ValidationError("Это имя уже занято")
        if User.objects.filter(email=data.get("email")).exists():
            raise serializers.ValidationError("Эта почта уже занята")
        return data

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                "Вы не можете использовать это имя"
            )
        return value


class TokenObtainWithConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


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

    def validate(self, data):
        if self.instance is None:
            title_id = self.context['view'].kwargs.get('title_id')
            reviews = get_object_or_404(Title, pk=title_id).reviews.all()
            if reviews.filter(
                author_id=self.context['request'].user.id
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение.'
                )
        return data
    



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        model = Comment
        exclude = ("review",)
