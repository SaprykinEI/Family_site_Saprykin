from django import forms
from django.template.defaultfilters import title

from django.utils.text import slugify
import uuid

from family_tree.utils import slug_generator

from gallery.models import Album, Category, Photo, Tag


class AlbumCreateForm(forms.ModelForm):
    """
        Форма для создания/редактирования объекта Album (альбома).
        Дополнительно:
        - new_category: поле для ввода новой категории, если нужной нет в списке;
        - new_tags: поле для ввода новых тегов через запятую.
        Сохраняет данные, создавая новые категории и теги при необходимости.
        """
    new_category = forms.CharField(
        max_length=100,
        required=False,
        label="Новая категория",
        help_text="Если нужной категории нет в списке, введите новую"
    )
    new_tags = forms.CharField(
        max_length=200,
        required=False,
        label="Новые теги",
        help_text="Введите новые теги через запятую, если их нет в списке"
    )

    class Meta:
        model = Album
        fields = ['title','location', 'cover_image', 'description',  'date', 'category', 'tags', 'is_active']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle-switch-checkbox'}),
        }

    def save(self, commit=True):
        """
         Переопределённый метод сохранения формы.
        1. Если у альбома нет слага — создаёт его.
        2. Если указана новая категория — создаёт/получает её и устанавливает для альбома.
        3. Сохраняет альбом и связи с тегами.
        4. Создаёт новые теги из строки new_tags, если они введены, и добавляет к альбому.
        """
        album = super().save(commit=False)

        if not album.slug:
            album.slug = slug_generator(album.title)

        new_category_name = self.cleaned_data.get('new_category')
        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name.strip())
            album.category = category

        if commit:
            album.save()
            self.save_m2m()

            new_tags_str = self.cleaned_data.get('new_tags', '')
            if new_tags_str:
                tag_names = [tag.strip() for tag in new_tags_str.split(',') if tag.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    album.tags.add(tag)

        return album


class PhotoUploadForm(forms.ModelForm):
    """ Форма для загрузки фотографий """
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'people', 'tags']
        widgets = {
            'people': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '6'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '6'}),
        }
