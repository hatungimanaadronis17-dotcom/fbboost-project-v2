import os
from django.core.wsgi import get_wsgi_application
# 🔧 Exécuter le fix admin une seule fois
import fbboost.fix_admin
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fbboost.settings')

application = get_wsgi_application()
