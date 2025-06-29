from django.conf import settings
from django.db import models
from django.utils import timezone
from family_tree.models import Person
from family_tree.utils import slug_generator

from users.models import NULLABLE


class Event(models.Model):
    REPEAT_CHOICES = [
        ('none', 'Не повторяется'),
        ('yearly', 'Каждый год'),
        ('custom', 'Каждые N лет'),
    ]

    EVENT_TYPE_CHOICES = [
        ('birthday', 'День рождения'),
        ('wedding', 'Свадьба'),
        ('anniversary', 'Юбилей'),
        ('memory', 'Памятное событие'),
        ('military', 'Армия / фронт'),
        ('death', 'Смерть'),
        ('study', 'Учёба / работа'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=255, verbose_name="Название события")
    date = models.DateField(verbose_name="Дата события")

    repeat = models.CharField(max_length=25, choices=REPEAT_CHOICES, default='none', verbose_name="Повтор")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='other', verbose_name="Тип события")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              related_name='events', verbose_name='Создатель события', **NULLABLE)
    people = models.ManyToManyField('family_tree.Person', blank=True,
                                    verbose_name="Связанные лица", related_name='events')
    categories = models.ManyToManyField('gallery.Category', blank=True, verbose_name="Категории")

    is_reminder_enabled = models.BooleanField(default=False, verbose_name="Напоминание включено")
    is_in_timeline = models.BooleanField(default=True, verbose_name="Показывать в хронологии")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"
        ordering = ('date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(self.title)
        super().save(*args, **kwargs)

