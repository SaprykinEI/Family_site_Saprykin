from django.core.management import BaseCommand

from users.models import User, UserRoles


class Command(BaseCommand):

    def handle(self, *args, **options):
        admin = User.objects.create(
            email='saprykin-family@yandex.com',
            first_name='Admin',
            last_name='Family-Site',
            role=UserRoles.ADMIN,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            is_verified=True,
        )

        admin.set_password('saprykinfamilysite')
        admin.save()
        print("Администратор создан")

        moderator = User.objects.create(
            email='moderator@yandex.com',
            first_name='Moderator',
            last_name='Moderator',
            role=UserRoles.MODERATOR,
            is_staff=True,
            is_superuser=False,
            is_active=True,
            is_verified=True,
        )

        moderator.set_password('saprykinfamilysite')
        moderator.save()
        print("Модератор создан")

        user = User.objects.create(
            email='user@yandex.com',
            first_name='User',
            last_name='User',
            role=UserRoles.USER,
            is_staff=False,
            is_superuser=True,
            is_active=True,
            is_verified=True,
        )

        user.set_password('saprykinfamilysite')
        user.save()
        print("Юзер создан")


