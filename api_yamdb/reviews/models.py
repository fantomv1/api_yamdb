from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()  # Временно для работы.


class Categories(models.Model):
    pass


class Title(models.Model):
    pass


class Genres(models.Model):
    pass


class GenreTitle(models.Model):
    pass


class Users(models.Model):
    pass


class Reviews(models.Model):
    pass


class Comments(models.Model):
    pass
