from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Help: For being possible to login in the system for the first time, you should, is necessary create a default user'
    help = "All the information about the username and the password is on the documentation"

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='default').exists():
            # Create the default user
            user = User.objects.create_user('default', 'default@example.com', 'password123')
            user.first_name = 'Default'
            user.last_name = 'User'
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully created user'))
        else:
            self.stdout.write(self.style.SUCCESS('User already exists'))
