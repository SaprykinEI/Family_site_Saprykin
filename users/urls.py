from django.urls import path

from users.apps import UsersConfig
from users.views import (UserRegisterView, UserLoginView, UserProfileView, UserLogoutView, UserUpdateView,
                         UserChangePasswordView, ConfirmEmailView, ResetPasswordView)

app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('register/', UserRegisterView.as_view(), name="user_register"),
    path('profile/', UserProfileView.as_view(), name="user_profile"),
    path('update/', UserUpdateView.as_view(), name="user_update"),
    path('change_password/', UserChangePasswordView.as_view(), name="user_change_password"),
    path('confirm_email/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),



]