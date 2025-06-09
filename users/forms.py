from django import forms

from users.models import User
from users.validators import validate_password
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm



class UserLoginForm(AuthenticationForm):
    pass


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email'

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        validate_password(cleaned_data['password1'])
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError("Пароли не совпадают!")
        return cleaned_data['password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'avatar')


class UserChangePasswordForm(PasswordChangeForm):
    pass


class ConfirmationCodeForm(forms.Form):
    code = forms.CharField(max_length=6)


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="Введите ваш email")