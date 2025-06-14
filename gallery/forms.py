from django import forms
from django.template.defaultfilters import title

from gallery.models import Album, Category, Photo


class AlbumCreateForm(forms.ModelForm):
    new_category = forms.CharField(max_length=100, required=False, label="Новая категория",
                                   help_text="Если нужной категории нет в списке, введите новую")

    class Meta:
        model = Album
        fields = ['title', 'cover_image', 'description', 'category', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        album = super().save(commit=False)

        new_category_name = self.cleaned_data['new_category']
        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name.strip())
            album.category = category

        if commit:
            album.save()
        return album


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'people', 'tags']
        widgets = {
            'people': forms.CheckboxSelectMultiple,
            'tags': forms.CheckboxSelectMultiple,
        }