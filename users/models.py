from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    ADMIN = 'admin',_('admin')
    MODERATOR = 'moderator',_('moderator')
    USER = 'user',_('user')


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER)
    first_name = models.CharField(max_length=150, verbose_name="Имя", default="Анонимный")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия", default="Пользователь")
    phone = models.CharField(max_length=20, verbose_name="Телефон", **NULLABLE)
    telegram = models.CharField(max_length=150, verbose_name="Телеграм", **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name="Фото профиля", **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name="Активность")
    is_verified = models.BooleanField(default=False, verbose_name="Подтверждение почты")
    confirmation_code = models.CharField(max_length=6, **NULLABLE, verbose_name="Код подтверждения")

    # Communication with a Person (one-to-one)
    person = models.OneToOneField('family_tree.Person', on_delete=models.SET_NULL, **NULLABLE, related_name='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']