from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string


def send_confirmation_email(email):
    """Сгенерировать случайный код."""
    confirmation_code = get_random_string(length=6)
    subject = 'Confirmation Code'
    message = f'Your confirmation code is: {confirmation_code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email,]
    # send_mail(subject, message, from_email, recipient_list, fail_silently=False,) # Выключаем реальную отправку сообщений.
    print("Почта:", email, "Код:", confirmation_code)  # Отправляем в консоль.
    return confirmation_code
