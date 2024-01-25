from django.core.exceptions import ValidationError


def validate_username(value):
    """Проверить правильность имени пользователя."""

    if not isinstance(value, str):
        raise ValidationError(
            'username должен иметь тип str'
        )
    if value.lower() == 'me':
        raise ValidationError(
            'username не может быть "me"'
        )
    return value
