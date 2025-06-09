from django.shortcuts import render, reverse, redirect
from django.http import  HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import ListView, UpdateView, DeleteView, FormView, TemplateView
from django.contrib.auth import get_user_model

User = get_user_model()

from users.forms import (UserRegisterForm, UserLoginForm, UserUpdateForm, UserChangePasswordForm, ConfirmationCodeForm,
                         ResetPasswordForm)
from users.services import send_confirmation_email, send_new_password, generate_new_password


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'users/user_register.html'
    success_url = reverse_lazy('users:confirm_email')
    extra_context = {
        'tittle': "Создайте новый аккаунт"
    }

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.set_password(form.cleaned_data['password1'])
        new_user.save()

        send_confirmation_email(new_user)
        # Сохраняем email нового пользователя во временное хранилище (сессию)
        self.request.session['pending_user_email'] = new_user.email
        messages.info(self.request, "Проверьте почту и введите код подтверждения")

        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/user_login.html'
    success_url = reverse_lazy('family_tree:index')
    extra_context = {
        'tittle': "Вход в аккаунт"
    }


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/user_profile.html'
    login_url = reverse_lazy('users:user_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.first_name and user.last_name:
            user_name = f"{user.first_name} {user.last_name}"
        else:
            user_name = "Анонимный пользователь"

        context['title'] = f"Ваш профиль: {user_name}"
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:user_profile')
    login_url = reverse_lazy('users:user_login')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['title'] = f"Изменить данные профиля {user.first_name} {user.last_name}"
        return context





@login_required(login_url='users:user_login')
def user_change_password_view(request):
    user_object = request.user
    form = UserChangePasswordForm(user_object, request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user_object = form.save()
            update_session_auth_hash(request, user_object)
            messages.success(request, "Пароль был успешно изменён!")
            return HttpResponseRedirect(reverse('users:user_profile'))
        else:
            messages.error(request, "Не удалось изменить пароль")
    context = {
        'title': f"Изменение пароля {user_object.first_name} {user_object.last_name}",
        'form': form
    }
    return render(request, 'users/user_change_password.html', context=context)


@login_required(login_url='users:user_login')
def user_logout_view(request):
    logout(request)
    return redirect('family_tree:index')


def confirm_email_view(request):
    form = ConfirmationCodeForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            code = form.cleaned_data['code']
            email = request.session.get('pending_user_email')

            if not email:
                messages.error(request, "Сессия истекла. Повторите регистрацию.")
                return redirect('users:user_register')

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Пользователь не найден.")
                return redirect('users:user_register')

            if user.confirmation_code == code:
                user.is_active = True
                user.is_verified = True
                user.confirmation_code = ''
                user.save()
                del request.session['pending_user_email']

                messages.success(request, "Email подтверждён. Добро пожаловать в семью!")
                return redirect('users:user_login')
            else:
                messages.error(request, "Неверный код подтверждения, попробуйте снова.")


    return render(request, 'users/confirm_email.html', {'form': form})


@login_required(login_url='users:user_login')
def reset_password_view(request):
    form = ResetPasswordForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Пользователь с таким email не найден.")
                return redirect('users:reset_password')

            new_password = generate_new_password()
            user.set_password(new_password)
            user.save()

            send_new_password(email, new_password)

            messages.success(request, "Новый пароль был отправлен на вашу почту.")
            return redirect('users:user_login')

    return render(request, 'users/reset_password.html', {'form': form})