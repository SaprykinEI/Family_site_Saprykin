from django import forms

from users.models import User
from users.validators import validate_password
from django.contrib.auth.forms import PasswordChangeForm



class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'password', 'password2'

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        validate_password(cleaned_data['password'])
        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError("Пароли не совпадают!")
        return cleaned_data['password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'avatar')


class UserChangePasswordForm(PasswordChangeForm):
    pass