from django.shortcuts import render, reverse, redirect
from django.http import  HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

from users.forms import (UserRegisterForm, UserLoginForm, UserUpdateForm, UserChangePasswordForm, ConfirmationCodeForm,
                         ResetPasswordForm)
from users.services import send_confirmation_email, send_new_password, generate_new_password


def user_register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = False  # Пользователь неактивен до подтверждения
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            send_confirmation_email(new_user)

            request.session['pending_user_email'] = new_user.email
            messages.info(request, 'Проверьте почту и введите код подтверждения')
            return redirect('users:confirm_email')
    else:
        form = UserRegisterForm()

    context = {
        'title': 'Создать аккаунт',
        'form': form
    }
    return render(request, 'users/user_register.html', context=context)


def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(email=cleaned_data['email'], password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('family_tree:index'))
            return HttpResponse("Вы не зарегистрированы, или ввели не верные данные.")
    context = {
        'title': 'Вход в аккаунт',
        'form': UserLoginForm
    }
    return render(request, 'users/user_login.html', context=context)


@login_required(login_url='users:user_login')
def user_profile_view(request):
    user_object = request.user
    if user_object.first_name and user_object.last_name:
        user_name = user_object.first_name + ' ' + user_object.last_name
    else:
        user_name = "Анонимный пользователь"
    context = {
        'title': f"Ваш профиль: {user_name}"
    }
    return render(request, 'users/user_profile.html', context=context)


@login_required(login_url='users:user_login')
def user_update_view(request):
    user_object = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user_object)
        if form.is_valid():
            user_object = form.save()
            user_object.save()
            return HttpResponseRedirect(reverse('users:user_profile'))
    context = {
        'object': user_object,
        'title': f"Изменить данные профиля {user_object.first_name} {user_object.last_name}",
        'form': UserUpdateForm(instance=user_object)
    }
    return render(request, 'users/user_update.html', context=context)


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