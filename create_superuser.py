# create_superuser.py
import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

def create_superuser():
    User = get_user_model()
    if os.environ.get('CREATE_SUPERUSER') == 'True':
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@fbboost.com',
                password='ton-mot-de-passe-tres-securise'
            )
            print("Superuser créé !")
        else:
            print("Superuser existe déjà")

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fbboost.settings')
    import django
    django.setup()
    create_superuser()
