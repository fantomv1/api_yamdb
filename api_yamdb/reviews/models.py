from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_username


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
        default="user",
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
        return self.role == "admin" or self.is_superuser

    @property
    def is_moder(self):
        return self.role == "moderator"


User = get_user_model()


class Category(models.Model):
    name = models.CharField("Название", max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self):
        return self.name[:15]


class Genre(models.Model):
    name = models.CharField("Название", max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ("name",)

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    name = models.CharField("Название", max_length=256)
    year = models.IntegerField(
        "Год выпуска",
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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("-pub_date",)
        constraints = (
            models.constraints.UniqueConstraint(
                fields=("title", "author"), name="unique_person"
            ),
        )

    def __str__(self):
        return f"{self.text[:10]} {self.author} {self.score}"


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)

    def __str__(self):
        return f"{self.text[:10]} {self.author}"
