from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон", **NULLABLE)
    telegram = models.CharField(max_length=150, verbose_name="Телеграм", **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name="Активность")

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