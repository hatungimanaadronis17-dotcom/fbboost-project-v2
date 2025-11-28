from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create superuser if not exists'

    def handle(self, *args, **options):
        if not User.objects.filter(username='Adronis4000').exists():
            User.objects.create_superuser('Adronis4000', '', 'boost2025')
            self.stdout.write(self.style.SUCCESS('Superuser Adronis4000 créé avec mot de passe boost2025'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser existe déjà'))
