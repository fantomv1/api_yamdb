from datetime import datetime

from django.core.exceptions import ValidationError

YEAR_ERROR = "Недействительный год выпуска!"


def validate_username(value):
    """Проверить правильность имени пользователя."""

    if not isinstance(value, str):
        raise ValidationError("username должен иметь тип str")
    if value.lower() == "me":
        raise ValidationError('username не может быть "me"')
    return value


def validate_year(value):
    if value > datetime.now().year:
        raise ValidationError(YEAR_ERROR)
    return value
