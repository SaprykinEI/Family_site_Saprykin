from django.shortcuts import render, reverse, redirect
from django.http import  HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import  UpdateView,  FormView, TemplateView, View
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


class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserChangePasswordForm
    template_name = 'users/user_change_password.html'
    success_url = reverse_lazy('users:user_profile')
    login_url = reverse_lazy('users:user_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['title'] = f"Изменение пароля {user.first_name} {user.last_name}"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Пароль был успешно изменён!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Не удалось изменить пароль!")
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    pass


class ConfirmEmailView(View):
    form_class = ConfirmationCodeForm
    template_name = 'users/confirm_email.html'
    success_url = reverse_lazy('users:user_login')
    error_url = reverse_lazy('users:user_register')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            email = request.session.get('pending_user_email')

            if not email:
                messages.error(request, "Сессия истекла. Повторите регистрацию")
                return redirect(self.error_url)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Пользователь не найден.")
                return redirect(self.error_url)

            if user.confirmation_code == code:
                user.is_active = True
                user.is_verified = True
                user.confirmation_code = ''
                user.save()
                del request.session['pending_user_email']

                messages.success(request, "Email подтверждён. Добро пожаловать в семью!")
                return redirect(self.success_url)
            else:
                messages.error(request, "Неверный код подтверждения, попробуйте снова.")
        return render(request, self.template_name, {'form': form})


class ResetPasswordView(View):
    form_class = ResetPasswordForm
    template_name = 'users/reset_password.html'
    success_url = reverse_lazy('users:user_login')
    error_url = reverse_lazy('users:reset_password')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Пользователь с таким email не найден.")
                return redirect(self.error_url)

            new_password = generate_new_password()
            user.set_password(new_password)
            user.save()

            send_new_password(email, new_password)
            messages.success(request, "Новый пароль был отправлен на вашу почту.")
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})
