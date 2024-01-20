from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


User_test = get_user_model()  # Временно для работы.


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:15]


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска',)
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Жанр',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория',
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year',)

    def __str__(self):
        return (
            f'{self.name[:10]} {self.year} {self.description[:20]}'
            f'{self.genre} {self.category}'
        )


class Users(models.Model):
    pass


class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        blank=True,  # Для теста.
        null=True,  # Для теста.
    )
    text = models.TextField()
    author = models.ForeignKey(
        User_test,
        on_delete=models.CASCADE,
        related_name="reviews",
        blank=True,  # Для теста.
        null=True,  # Для теста.
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )  # Временно, до реализации подсчета рейтинга.
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        blank=True,  # Для теста.
        null=True,  # Для теста.
    )
    text = models.TextField()
    author = models.ForeignKey(
        User_test,
        on_delete=models.CASCADE,
        related_name="comments",
        blank=True,  # Для теста.
        null=True,  # Для теста.
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
