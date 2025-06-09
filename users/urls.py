from django.urls import path

from users.apps import UsersConfig
from users.views import (UserRegisterView, UserLoginView, UserProfileView, user_logout_view, UserUpdateView,
                         user_change_password_view, confirm_email_view, reset_password_view)

app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(), name='user_login'),
    path('logout/', user_logout_view, name='user_logout'),
    path('register/', UserRegisterView.as_view(), name="user_register"),
    path('profile/', UserProfileView.as_view(), name="user_profile"),
    path('update/', UserUpdateView.as_view(), name="user_update"),
    path('change_password/', user_change_password_view, name="user_change_password"),
    path('confirm_email/', confirm_email_view, name='confirm_email'),
    path('reset_password/', reset_password_view, name='reset_password'),



]