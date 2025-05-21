from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        admin_user = User.objects.create(
            email='saprykin-family@yandex.com',
            first_name='Admin',
            last_name='Family-Site',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        admin_user.set_password('saprykinfamilysite')
        admin_user.save()
        print("Администратор создан")
