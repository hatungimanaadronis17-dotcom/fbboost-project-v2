import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fbboost.settings')

# Appliquer automatiquement les migrations
try:
    call_command('migrate', interactive=False)
    print("✅ Migrations appliquées avec succès")
except Exception as e:
    # Affiche l'erreur sans empêcher le serveur de démarrer
    print(f"⚠️ Échec des migrations : {e}")

application = get_wsgi_application()
