import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Create a Render superuser if one does not already exist.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'anshika')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'anshika@gmail.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'anshika')

        identifier = {User.USERNAME_FIELD: username} if User.USERNAME_FIELD != 'email' else {'email': email}
        if User.objects.filter(email=email).exists() or User.objects.filter(**identifier).exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists.'))
            return

        create_kwargs = {
            'email': email,
            'password': password,
        }

        if User.USERNAME_FIELD != 'email':
            create_kwargs['username'] = username

        try:
            User.objects.create_superuser(**create_kwargs)
            self.stdout.write(self.style.SUCCESS(f'Superuser created: {email}'))
        except TypeError:
            if 'username' in create_kwargs:
                create_kwargs.pop('username')
                User.objects.create_superuser(**create_kwargs)
                self.stdout.write(self.style.SUCCESS(f'Superuser created: {email}'))
            else:
                raise
        except IntegrityError as exc:
            self.stdout.write(self.style.WARNING(f'Superuser creation skipped: {exc}'))
