from django import forms

from family_tree.models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ['creator']