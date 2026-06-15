from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates the default user for first-time setup'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='default').exists():
            User.objects.create_user(
                username='default',
                email='default@example.com',
                password='password123'
            )
            self.stdout.write(self.style.SUCCESS('Default user created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Default user already exists'))
