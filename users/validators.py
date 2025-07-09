import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.templatetags.i18n import language


def validate_password(value):
    """ Проверяет валидность пароля.
        Правила:
        - Длина должна быть от 8 до 16 символов включительно.
        - Пароль должен содержать только латинские буквы и цифры.
        В случае ошибки выбрасывает ValidationError с сообщением на текущем языке. """
    language = settings.LANGUAGE_CODE
    error_messages = [
        {
            'ru-ru': "Пароль должен содержать от 8 до 16 символов",
            'en-us': "The password must contain from 8 to 16 characters."
        },
        {
            'ru-ru': "Пароль должен содержать только латинские буквы и цифры",
            'en-us': "The password must contain only Latin letters and numbers."
        }
    ]
    try:
        if not 8 <= len(value) <= 16:
            raise ValidationError(error_messages[0]['language'])

        pattern = re.compile(r'^[a-zA-Z0-9]+$')
        if not pattern.fullmatch(value):
            raise ValidationError(error_messages[1]['language'])
    except KeyError:
        print("Не знаю такого языка")
