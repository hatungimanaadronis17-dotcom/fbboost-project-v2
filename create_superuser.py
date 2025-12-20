# create_superuser.py - À la racine du projet (même niveau que manage.py)
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fbboost.settings')
django.setup()

from django.contrib.auth.models import User

# ==== PARAMÈTRES DU SUPERUSER ====
USERNAME = "kingston"                  # Change si tu veux
EMAIL = "kingston@fbboost.com"         # Email (peut être fake)
PASSWORD = "Kingston2025@fbboost!"     # Mot de passe très fort

# ==== CRÉATION ====
try:
    if User.objects.filter(username=USERNAME).exists():
        print(f"[SUPERUSER] Le superuser '{USERNAME}' existe déjà.")
    else:
        User.objects.create_superuser(username=USERNAME, email=EMAIL, password=PASSWORD)
        print(f"[SUPERUSER] Superuser '{USERNAME}' créé avec succès !")
        print(f"    → Username : {USERNAME}")
        print(f"    → Password : {PASSWORD}")
        print("    → Tu peux te connecter sur /admin/")
except Exception as e:
    print(f"[ERREUR] Impossible de créer le superuser : {e}")
