from django.db import models
from django.conf import settings

from family_tree.models import Person
from users.models import NULLABLE

from gallery.utils import photo_upload_path, video_upload_path


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Тег")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Название категории")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    color = models.CharField(max_length=20, **NULLABLE, verbose_name="Цвет")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']


class Album(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название альбома")
    date = models.DateField(verbose_name="Дата")
    location = models.CharField(max_length=255, **NULLABLE, verbose_name="Локация")
    description = models.TextField(**NULLABLE, verbose_name="Описание альбома")
    cover_image = models.ImageField(upload_to='album_covers/', verbose_name="Обложка альбома")
    created_at = models.DateTimeField(auto_now_add=True, **NULLABLE, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активность альбома")

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,  **NULLABLE,
                                related_name='albums', verbose_name='Владелец альбома')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, **NULLABLE,
                                 related_name='albums', verbose_name="Категория")
    tags = models.ManyToManyField(Tag, blank=True, related_name='albums', verbose_name="Теги")


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"


class Photo(models.Model):
    image = models.ImageField(upload_to=photo_upload_path, verbose_name="Фотография")
    caption = models.CharField(max_length=255, **NULLABLE, verbose_name="Подпись")
    date_taken = models.DateField(**NULLABLE, verbose_name="Дата")

    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos', verbose_name="Привязка к альбому")
    people = models.ManyToManyField('family_tree.Person', **NULLABLE,
                                    related_name='photos', verbose_name="Привязка к карточке")
    tags = models.ManyToManyField('Tag', **NULLABLE, related_name='photos', verbose_name="Привязка к тегам")

    def __str__(self):
        return self.caption or f"Фото от {self.date_taken}"

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"


class Video(models.Model):
    file = models.FileField(upload_to=video_upload_path, **NULLABLE, verbose_name="Видео")
    url = models.URLField(**NULLABLE, verbose_name="Ссылка на видео")
    caption = models.CharField(max_length=255, **NULLABLE, verbose_name="Подпись")
    date_taken = models.DateField(**NULLABLE, verbose_name="Дата")

    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='videos', verbose_name="Привязка к альбому")
    people = models.ManyToManyField('family_tree.Person', **NULLABLE,
                                    related_name='videos', verbose_name="Привязка к карточке")
    tags = models.ManyToManyField('Tag', **NULLABLE, related_name='videos', verbose_name="Привязка к тегам")

    def __str__(self):
        return self.caption or f"Видео от {self.date_taken}"

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"