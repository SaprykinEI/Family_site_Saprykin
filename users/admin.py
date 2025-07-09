from django.contrib import admin
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Класс админки для модели User.
     Позволяет удобно управлять пользователями из административной панели Django """
    list_display = ('pk', 'email', 'last_name', 'first_name', 'role', 'is_active' )
    list_filter = ('last_name', 'first_name',)
    search_fields = ('first_name', 'last_name')

