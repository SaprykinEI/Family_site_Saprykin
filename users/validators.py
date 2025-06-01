import re
from django.core.exceptions import ValidationError


def validate_password(value):
    if not 8 <= len(value) <= 16:
        raise ValidationError("Пароль должен содержать от 8 до 16 символов")

    pattern = re.compile(r'^[a-zA-Z0-9]+$')
    if not pattern.fullmatch(value):
        raise ValidationError("Пароль должен содержать только латинские буквы и цифры")
