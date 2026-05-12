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

        username_field = getattr(User, 'USERNAME_FIELD', 'username')
        has_email_field = any(field.name == 'email' for field in User._meta.fields)

        identifier = {username_field: username}
        if has_email_field:
            identifier['email'] = email

        if User.objects.filter(**identifier).exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists.'))
            return

        create_kwargs = {'password': password}

        if username_field != 'email':
            create_kwargs[username_field] = username
            if has_email_field:
                create_kwargs['email'] = email
        else:
            create_kwargs['email'] = email

        try:
            User.objects.create_superuser(**create_kwargs)
            self.stdout.write(self.style.SUCCESS(f'Superuser created: {email}'))
        except TypeError:
            if username_field != 'email' and username_field in create_kwargs:
                create_kwargs.pop(username_field)
                User.objects.create_superuser(**create_kwargs)
                self.stdout.write(self.style.SUCCESS(f'Superuser created: {email}'))
            else:
                raise
        except IntegrityError as exc:
            self.stdout.write(self.style.WARNING(f'Superuser creation skipped: {exc}'))
