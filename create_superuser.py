# create_superuser.py
import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Crée un superuser si il n\'existe pas'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'Adronis')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'evelyneirambona66@gmail.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'hatu1578ngimana')

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" existe déjà.'))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" créé avec succès.'))
