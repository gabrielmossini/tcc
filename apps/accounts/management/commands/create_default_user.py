from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.accounts.models import Profile

class Command(BaseCommand):
    help = 'Creates the default user for first-time setup'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='default').exists():
            user = User.objects.create_user(
                username='default',
                email='default@example.com',
                password='password123'
            )
            user.first_name = 'Default'
            user.last_name = 'User'
            user.save()

            Profile.objects.create(
                user=user,
                name='Default User',
                cpf='000.000.000-00',
                birthday='1990-01-01'
            )
            self.stdout.write(self.style.SUCCESS('Default user and profile created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Default user already exists'))