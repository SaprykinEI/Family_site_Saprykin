from django.db import models
from django.conf import settings


from family_tree.models import Person
from family_tree.utils import slug_generator
from users.models import NULLABLE, User

from gallery.utils import photo_upload_path, video_upload_path


class Tag(models.Model):
    """ Модель Тег для обозначения меток, которые можно присваивать альбомам. """
    name = models.CharField(max_length=100, unique=True, verbose_name="Тег")

    def __str__(self):
        """Возвращает строковое представление объекта, в данном случае — просто название тега."""
        return self.name

    class Meta:
        """ Дополнительные настройки модели: """
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Category(models.Model):
    """ Модель Категория для группировки альбомов, фото или других объектов. """
    name = models.CharField(max_length=200, unique=True, verbose_name="Название категории")
    description = models.TextField(**NULLABLE, verbose_name="Описание")
    color = models.CharField(max_length=20, **NULLABLE, verbose_name="Цвет")

    def __str__(self):
        """ Метод возвращает строковое представление объекта.
        Нужно, чтобы удобно было видеть категорию в списках. """
        return self.name

    class Meta:
        """ Дополнительные настройки модели: """
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']


class Album(models.Model):
    """   Модель Альбом — это коллекция фотографий или видео. """
    title = models.CharField(max_length=200, verbose_name="Название альбома")
    date = models.DateField(verbose_name="Дата")
    location = models.CharField(max_length=255, **NULLABLE, verbose_name="Локация")
    description = models.TextField(**NULLABLE, verbose_name="Описание альбома")
    cover_image = models.ImageField(upload_to='album_covers/', verbose_name="Обложка альбома")
    created_at = models.DateTimeField(auto_now_add=True, **NULLABLE, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активность альбома")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Слаг")
    views = models.IntegerField(default=0, verbose_name="Просмотры")


    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,  **NULLABLE,
                                related_name='albums', verbose_name='Владелец альбома')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, **NULLABLE,
                                 related_name='albums', verbose_name="Категория")
    tags = models.ManyToManyField(Tag, blank=True, related_name='albums', verbose_name="Теги")

    def save(self, *args, **kwargs):
        """ Автоматическое создание слага """
        if not self.slug:
            self.slug = slug_generator(self.title)
        super().save(*args, **kwargs)

    @property
    def like_count(self):
        """ Возвращает количество лайков альбома. """
        return self.likes.count()

    def __str__(self):
        """ Строковое представление объекта — название альбома. """
        return self.title

    def increment_view_count(self):
        """ Увеличивает счётчик просмотров альбома на 1 и сохраняет изменение. """
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"


class AlbumLike(models.Model):
    """ Модель Лайк для альбома. """
    album =models.ForeignKey(Album, on_delete=models.CASCADE, related_name='likes', verbose_name="Лайк")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Привязка к User")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        unique_together = ('album', 'user')

    def __str__(self):
        """ Строковое представление лайка — показывает, какой пользователь поставил лайк какому альбому. """
        return f"{self.user} likes {self.album}"


class Photo(models.Model):
    """ Модель Фотография.
    Хранит информацию о фото: файл изображения, подпись, дату съемки,
    а также связи с альбомом, людьми на фото и тегами. """
    image = models.ImageField(upload_to=photo_upload_path, verbose_name="Фотография")
    caption = models.CharField(max_length=255, **NULLABLE, verbose_name="Подпись")
    date_taken = models.DateField(**NULLABLE, verbose_name="Дата")

    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos', verbose_name="Привязка к альбому")
    people = models.ManyToManyField('family_tree.Person', blank=True,
                                    related_name='photos', verbose_name="Привязка к карточке")
    tags = models.ManyToManyField('Tag', blank=True, related_name='photos', verbose_name="Привязка к тегам")

    def __str__(self):
        """Строковое представление объекта — подпись к фото,
        или если подписи нет, то "Фото от {дата}"."""
        return self.caption or f"Фото от {self.date_taken}"

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"


class Video(models.Model):
    """ Модель Видео.
        Хранит информацию о видеоролике: сам файл или ссылку на видео, подпись, дату съемки,
        а также связи с альбомом, изображёнными людьми и тегами."""
    file = models.FileField(upload_to=video_upload_path, **NULLABLE, verbose_name="Видео")
    url = models.URLField(**NULLABLE, verbose_name="Ссылка на видео")
    caption = models.CharField(max_length=255, **NULLABLE, verbose_name="Подпись")
    date_taken = models.DateField(**NULLABLE, verbose_name="Дата")

    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='videos', verbose_name="Привязка к альбому")
    people = models.ManyToManyField('family_tree.Person', blank=True,
                                    related_name='videos', verbose_name="Привязка к карточке")
    tags = models.ManyToManyField('Tag', blank=True, related_name='videos', verbose_name="Привязка к тегам")

    def __str__(self):
        return self.caption or f"Видео от {self.date_taken}"

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
