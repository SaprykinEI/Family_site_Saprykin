from django.urls import path

from users.apps import UsersConfig
from users.views import user_register_view, user_login_view


app_name = UsersConfig.name

urlpatterns = [
    path('', user_login_view, name='user_login'),
    path('register/', user_register_view, name="user_register"),

]