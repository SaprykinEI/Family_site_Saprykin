from django.contrib import admin
from family_tree.models import Person


@admin.register(Person)
class UserAdmin(admin.ModelAdmin):
    """ Настройка отображения модели Person в административной панели Django. """
    list_display = ('last_name', 'first_name', 'pk', 'creator')
    list_filter = ('last_name',)
    search_fields = ('first_name', 'last_name')
    ordering = ('last_name', 'first_name')
    prepopulated_fields = {'slug': ('last_name', 'first_name')}
