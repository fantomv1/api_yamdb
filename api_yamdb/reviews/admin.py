from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import User

# Добавляем поля
# к стандартному набору полей (fieldsets) пользователя в админке.
UserAdmin.fieldsets += (
    # Добавляем кортеж, где первый элемент — это название раздела в админке,
    # а второй элемент — словарь, где указать нужные поля.
    ("Extra Fields", {"fields": ("bio", "role")}),
)
# Регистрируем модель в админке:
admin.site.register(User, UserAdmin)
