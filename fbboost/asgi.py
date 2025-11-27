import os
from django.core.assgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fbboost.settings')

application = get_asgi_application()
