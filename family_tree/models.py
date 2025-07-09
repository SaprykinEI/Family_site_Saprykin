from PIL import Image, ExifTags
from django.db import models
from django.conf import settings

from family_tree.utils import slug_generator
from users.models import NULLABLE


class Person(models.Model):
    """Модель члена семьи"""
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    maiden_name = models.CharField(max_length=50, **NULLABLE, verbose_name="Девичья фамилия")
    patronymic = models.CharField(max_length=50, **NULLABLE, verbose_name="Отчество")
    birth_date = models.DateField(verbose_name="Дата рождения")
    birth_place = models.CharField(max_length=100, **NULLABLE, verbose_name="Место рождения")
    death_date = models.DateField(**NULLABLE, verbose_name="Дата Смерти")
    photo = models.ImageField(upload_to="person_photos/", **NULLABLE, verbose_name="Фотография")
    photo_other = models.ImageField(upload_to="person_other_photos/", **NULLABLE, verbose_name="Фотография_2")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    bio = models.TextField(**NULLABLE, verbose_name="Биография")
    profession = models.CharField(max_length=150, **NULLABLE, verbose_name="Профессия")
    favorite_food = models.CharField(max_length=150, **NULLABLE, verbose_name="Любимая еда")
    playlist = models.URLField(**NULLABLE, verbose_name="Любимая музыка")
    hobbies = models.CharField(max_length=500, **NULLABLE, verbose_name="Хобби")
    slug = models.SlugField(max_length=255, unique=True, blank=True)


    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                related_name='created_people', **NULLABLE, verbose_name="Создатель карточки")
    mother = models.ForeignKey('self', on_delete=models.SET_NULL,
                               related_name='children_from_mother', **NULLABLE, verbose_name="Мать")
    father = models.ForeignKey('self', on_delete=models.SET_NULL,
                               related_name='children_from_father', **NULLABLE, verbose_name="Отец")
    spouse = models.ForeignKey('self', on_delete=models.SET_NULL,
                               related_name='spouses', **NULLABLE, verbose_name="Супруг(а)")

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        """Возвращает полное имя человека. Формирует строку формата ФИО """
        parts = [self.last_name, self.first_name]
        if self.patronymic:
            parts.append(self.patronymic)
        return " ".join(parts)

    def save(self, *args, **kwargs):
        """
        Сохраняет объект Person в базе данных.
        - Если поле slug пустое, автоматически генерирует его из фамилии и имени.
        - После сохранения уменьшает размер загруженных фотографий (photo и photo_other),
            чтобы они были не больше 800x800 и правильно ориентированы.
        """
        if not self.slug:
            full_name = f"{self.last_name} {self.first_name}"
            self.slug = slug_generator(full_name)
        super().save(*args, **kwargs)

        if self.photo:
            self.resize_image(self.photo.path)

        if self.photo_other:
            self.resize_image(self.photo_other.path)

    def resize_image(self, path):
        """
        Изменяет размер и ориентацию изображения по указаному пути
        - Проверяет EXIF-ориентацию и поворачивает фото
        - Уменьшает размер фото до 800х800 пикселей, сохраняя пропорции
        - Сохраняет фото обратно на диск с качеством 85%

        Используется для оптимизации фотографий при сохранении модели.
        """
        try:
            img = Image.open(path)
            # Попытка получить ориентацию из EXIF
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = img._getexif()
                if exif is not None:
                    orientation_value = exif.get(orientation, None)

                    if orientation_value == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation_value == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation_value == 8:
                        img = img.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                pass

            max_size = (800, 800)
            img.thumbnail(max_size, Image.LANCZOS)

            img.save(path, quality=85)
        except Exception as e:
            print(f"Error resizing image: {e}")

    def children(self):
        """
         Возвращает QuerySet всех детей этого человека.
         Ищет людей в базе, у которых отец или мать - это этот человек.
         """
        return Person.objects.filter(models.Q(father=self) | models.Q(mother=self))

    def get_absolute_url(self):
        """ Возвращает ссылку на страницу с подробной информацией об этом человеке. """
        from django.urls import reverse
        return reverse('person_detail', kwargs={'slug': self.slug})

    class Meta:
        """ Мета-настройки модели Person: """
        verbose_name = "Человек"
        verbose_name_plural = "Люди"
        ordering = ['last_name', 'first_name']
