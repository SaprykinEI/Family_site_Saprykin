from django import forms

from family_tree.models import Person


class PersonForm(forms.ModelForm):
    """ Форма для создания и редактирования объекта Person. """
    class Meta:
        """ Использует все поля модели Person, кроме 'creator' и 'slug', """
        model = Person
        exclude = ['creator', 'slug']
