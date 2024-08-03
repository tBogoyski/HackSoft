import random

from django.core.management import BaseCommand

from management.dummy_data_manager import GenerateDummyDataManager
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Generate dummy data used for manual testing purposes.'

    def handle(self, *args, **kwargs):
        data_manager = GenerateDummyDataManager()
        data_manager.generate_users()
        self.stdout.write(self.style.SUCCESS('Users generated successfully.'))
        superuser = random.choice(CustomUser.objects.filter(is_superuser=True, is_valid=True))
        self.stdout.write(self.style.SUCCESS('Random superuser for logging in the admin panel:'))
        self.stdout.write(self.style.SUCCESS(f'{superuser.email}'))
        self.stdout.write(self.style.SUCCESS('With password: 123456'))

        data_manager.generate_posts()
        self.stdout.write(self.style.SUCCESS('Posts generated successfully.'))
