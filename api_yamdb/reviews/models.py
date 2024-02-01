from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.numbers import (
    MAX_LEN_NAME,
    MAX_LEN_ROLE,
    MAX_LEN_STR,
    MAX_LEN_USERNAME,
    MAX_SCORE,
    MIN_SCORE,
)
from reviews.validators import validate_username, validate_year


class User(AbstractUser):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

    ROLE_CHOICES = [
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
        (USER, "Пользователь"),
    ]

    username = models.CharField(
        "Пользователь",
        max_length=MAX_LEN_USERNAME,
        unique=True,
        validators=(validate_username, UnicodeUsernameValidator()),
    )
    email = models.EmailField(
        "Почта",
        unique=True,
    )
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.CharField(
        "Роль",
        max_length=MAX_LEN_ROLE,
        default=USER,
        choices=ROLE_CHOICES,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self):
        return self.username[:MAX_LEN_STR]

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moder(self):
        return self.role == self.MODERATOR


class CategoryGenreModel(models.Model):
    name = models.CharField("Название", max_length=MAX_LEN_NAME)
    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self):
        return self.name[:MAX_LEN_STR]


class Category(CategoryGenreModel):
    class Meta(CategoryGenreModel.Meta):
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(CategoryGenreModel):
    class Meta(CategoryGenreModel.Meta):
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    name = models.CharField("Название", max_length=MAX_LEN_NAME)
    year = models.SmallIntegerField("Год выпуска", validators=[validate_year])
    description = models.TextField("Описание", null=True, blank=True)
    genre = models.ManyToManyField(
        Genre, blank=True, through="GenreTitle", verbose_name="Жанр"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Категория",
        related_name="titles",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ("-year",)

    def __str__(self):
        return self.name[:MAX_LEN_STR]


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class ReviewCommentModel(models.Model):
    text = models.TextField(
        verbose_name="Текст",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор"
    )

    class Meta:
        abstract = True
        ordering = ("-pub_date",)


class Review(ReviewCommentModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Произведение",
    )
    score = models.PositiveSmallIntegerField(
        default=None,
        help_text="Оценка должна быть от 1 до 10.",
        verbose_name="Оценка",
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE),
        ],
    )

    class Meta(ReviewCommentModel.Meta):
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = (
            models.constraints.UniqueConstraint(
                fields=("title", "author"), name="unique_person"
            ),
        )
        default_related_name = "reviews"

    def __str__(self):
        return self.title[:MAX_LEN_STR]


class Comment(ReviewCommentModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )

    class Meta(ReviewCommentModel.Meta):
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        default_related_name = "comments"

    def __str__(self):
        return self.review[:MAX_LEN_STR]
