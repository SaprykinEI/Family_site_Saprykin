from django.db import models

from users.models import NULLABLE


class Person(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    patronymic = models.CharField(max_length=50, **NULLABLE, verbose_name="Patronymic")
    birth_date = models.DateField(verbose_name="Birth Date")
    death_date = models.DateField(**NULLABLE, verbose_name="Death Date")
    photo = models.ImageField(upload_to="photos/", **NULLABLE, verbose_name="Photo")
    bio = models.TextField(**NULLABLE, verbose_name="Bio")
    profession = models.CharField(max_length=150, **NULLABLE, verbose_name="Profession")
    favorite_food = models.CharField(max_length=150, **NULLABLE)
    playlist = models.URLField(**NULLABLE, verbose_name="music")
    hobbies = models.CharField(max_length=500, **NULLABLE, verbose_name="Hobby")

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
        verbose_name_plural = "People"
        ordering = ['last_name', 'first_name']

