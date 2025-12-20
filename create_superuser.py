# create_superuser.py
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fbboost.settings')
django.setup()

from django.contrib.auth.models import User

# Paramètres du superuser
USERNAME = "kingston"                     # ← Change si tu veux un autre nom
EMAIL = "kingston@fbboost.com"            # ← Ton email
PASSWORD = "Kingston2025@fbboost"         # ← Mot de passe fort

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print(f"SUPERUSER CRÉÉ AVEC SUCCÈS !")
    print(f"Username : {USERNAME}")
    print(f"Password : {PASSWORD}")
    print("Tu peux maintenant te connecter à /admin/")
else:
    print(f"Le superuser '{USERNAME}' existe déjà.")
