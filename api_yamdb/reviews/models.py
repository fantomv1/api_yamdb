from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models

from reviews.validators import validate_username


YEAR_ERROR = "Недействительный год выпуска!"


class MyUser(AbstractUser):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

    ROLE_CHOICES = [
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
        (USER, "Пользователь"),
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(validate_username, UnicodeUsernameValidator()),
    )
    email = models.EmailField(
        "Почта",
        unique=True,
    )
    bio = models.CharField(
        "Биография",
        max_length=255,
        blank=True,
    )
    role = models.CharField(
        max_length=50,
        default=USER,
        choices=ROLE_CHOICES,
    )
    confirmation_code = models.CharField(
        "Код подтверждения",
        max_length=6,
    )

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        return self.username[:15]

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moder(self):
        return self.role == self.MODERATOR


User = get_user_model()


class CategoryGenreModel(models.Model):
    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self):
        return self.name[:15]


class Category(CategoryGenreModel):
    name = models.CharField("Название", max_length=256)

    class Meta(CategoryGenreModel.Meta):
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(CategoryGenreModel):
    name = models.CharField("Название", max_length=256)

    class Meta(CategoryGenreModel.Meta):
        verbose_name_plural = "Жанры"


def validate_year(value):
    if value > datetime.now().year:
        raise ValidationError(YEAR_ERROR)
    return value


class Title(models.Model):
    name = models.CharField("Название", max_length=256)
    year = models.SmallIntegerField(
        "Год выпуска",
        validators=[validate_year]
    )
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
        return (
            f"{self.name[:10]} {self.year} {self.description[:20]}"
            f"{self.genre} {self.category}"
        )


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class ReviewCommentModel(models.Model):
    text = models.TextField(verbose_name="Текст",)
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ("-pub_date",)


class Review(ReviewCommentModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.PositiveSmallIntegerField(
        default=None,
        help_text="Оценка должна быть от 1 до 10.",
        verbose_name="Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta(ReviewCommentModel.Meta):
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = (
            models.constraints.UniqueConstraint(
                fields=("title", "author"), name="unique_person"
            ),
        )

    def __str__(self):
        return f"{self.text[:10]} {self.author} {self.score}"


class Comment(ReviewCommentModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )

    class Meta(ReviewCommentModel.Meta):
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"{self.text[:10]} {self.author}"
