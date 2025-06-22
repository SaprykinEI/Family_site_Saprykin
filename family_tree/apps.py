from django.apps import AppConfig


class FamilyTreeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'family_tree'

    def ready(self):
        import family_tree.signals
