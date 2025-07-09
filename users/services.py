import random
import string

from django.contrib.messages.context_processors import messages
from django.core.mail import send_mail
from django.conf import settings

def generate_confirmation_code():
    """Генерация случайного 6-значного кода"""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def generate_new_password():
    """Генерация нового пароля"""
    return ''.join(random.sample(string.ascii_letters + string.digits, 12))


def send_confirmation_email(user):
    """Отправка письма пользователю с кодом подтверждения"""
    code = generate_confirmation_code()
    user.confirmation_code = code
    user.save()

    subject = "Подтверждение регистрации"
    message = f'''Здравствуйте, {user.first_name} {user.last_name}!
                Вы зарегистрировались на семейном сайте семьи 'Сапрыкиных'.
                
                Ваш код подтверждения: {code}

                Если вы не регистрировались - проигнорируйте это сообщение.'''

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_new_password(email, new_password):
    """ Отправка письма пользователю с новым паролем """
    send_mail(
        subject="Вы успешно изменили пароль",
        message=f"Ваш новый пароль: {new_password}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )


