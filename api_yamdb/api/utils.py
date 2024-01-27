from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model


def send_confirmation_email(email):
    """Сгенерировать и отправить токен подтверждения."""
    user = get_user_model().objects.get(email=email)
    confirmation_token = default_token_generator.make_token(user)
    
    subject = "Код подтверждения"
    message = f"Ваш код подтверждения: {confirmation_token}"
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
    
    return confirmation_token
