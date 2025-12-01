import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fbboost.settings")
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@fbboost.com", "FbBoost2025@admin")
    print("SUPERUSER ADMIN CRÉÉ – Mot de passe : FbBoost2025@admin")
else:
    print("Superuser admin déjà existant")
