from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from users.models import User
from users.validators import validate_password
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm



class UserLoginForm(AuthenticationForm):
    """ Форма входа пользователя. """
    pass


class UserRegisterForm(UserCreationForm):
    """ Форма регистрации нового пользователя. """
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email'

    def clean_password2(self):
        """ Метод валидации пароля """
        cleaned_data = self.cleaned_data
        validate_password(cleaned_data['password1'])
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError("Пароли не совпадают!")
        return cleaned_data['password2']


class UserUpdateForm(forms.ModelForm):
    """ Форма для редактирования профиля пользователя. """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'avatar')


class UserChangePasswordForm(PasswordChangeForm):
    """ Форма смены пароля. """
    def clean_new_password2(self):
        """Переопределён метод clean_new_password2 для:
        - проверки совпадения нового пароля и его подтверждения,
        - проверки безопасности пароля встроенными валидаторами Django. """
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        password_validation.validate_password(password2, self.user)
        return password2


class ConfirmationCodeForm(forms.Form):
    """ Простая форма для ввода кода подтверждения (например, из письма).
        Содержит одно поле:
            - code: строка до 6 символов. """
    code = forms.CharField(max_length=6)


class ResetPasswordForm(forms.Form):
    """ Форма для запроса сброса пароля по email.
        Содержит одно поле email с русским лейблом. """
    email = forms.EmailField(label="Введите ваш email")