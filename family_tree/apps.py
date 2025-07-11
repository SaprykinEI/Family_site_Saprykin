from django.apps import AppConfig


class FamilyTreeConfig(AppConfig):
    """ Конфигурация приложения 'family_tree'. """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'family_tree'

    def ready(self):
        """ Метод, который вызывается при полной загрузке приложения. """
