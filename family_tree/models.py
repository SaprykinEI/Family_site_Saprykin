from django.db import models

from users.models import NULLABLE


class Person(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    maiden_name = models.CharField(max_length=50, **NULLABLE, verbose_name="Девичья фамилия")
    patronymic = models.CharField(max_length=50, **NULLABLE, verbose_name="Отчество")
    birth_date = models.DateField(verbose_name="Дата рождения")
    death_date = models.DateField(**NULLABLE, verbose_name="Дата Смерти")
    photo = models.ImageField(upload_to="photos/", **NULLABLE, verbose_name="Фотография")
    bio = models.TextField(**NULLABLE, verbose_name="Биография")
    profession = models.CharField(max_length=150, **NULLABLE, verbose_name="Профессия")
    favorite_food = models.CharField(max_length=150, **NULLABLE, verbose_name="Любимая еда")
    playlist = models.URLField(**NULLABLE, verbose_name="Любимая музыка")
    hobbies = models.CharField(max_length=500, **NULLABLE, verbose_name="Хобби")

    # mother = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='children_from_mother', **NULLABLE)
    # father = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='children_from_father', **NULLABLE)
    # spouse = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='spouses', **NULLABLE)

    def __str__(self):
        parts = [self.first_name, self.last_name]
        if self.patronymic:
            parts.append(self.patronymic)
        return " ".join(parts)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"
        ordering = ['last_name', 'first_name']

