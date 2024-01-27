from django.contrib.auth import get_user_model
from rest_framework import serializers

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


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )


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

    def create(self, validated_data):
        title = self.context["title"]
        author = self.context["author"]
        if Review.objects.filter(
            title=title,
            author=author
        ).exists():
            raise serializers.ValidationError("Отзыв уже создан.")
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        model = Comment
        exclude = ("review",)
