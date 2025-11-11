from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import secrets
import string

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a temporary superuser with a random password.'

    def handle(self, *args, **options):
        username = 'temp_admin'
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} already exists.'))
            return

        # Generate a random password
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(12))

        User.objects.create_superuser(username, f'{username}@example.com', password)

        self.stdout.write(self.style.SUCCESS(f'Successfully created temporary superuser.'))
        self.stdout.write(self.style.SUCCESS(f'Username: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
        self.stdout.write(self.style.WARNING('Please use these credentials to log in and create a permanent superuser. Then, remove this temporary command and URL.'))
