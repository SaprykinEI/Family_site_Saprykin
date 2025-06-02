from django.shortcuts import render, reverse, redirect
from django.http import  HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserChangePasswordForm


def user_register_view(request):
    form = UserRegisterForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save()
            print(new_user)
            print(form.cleaned_data['password'])
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return HttpResponseRedirect(reverse('users:user_login'))
    context = {
        'title': 'Создать аккаунт',
        'form': UserRegisterForm
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


@login_required
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


@login_required
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


@login_required
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


@login_required
def user_logout_view(request):
    logout(request)
    return redirect('family_tree:index')