
# exchange/apps.py
from django.apps import AppConfig


class ExchangeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exchange'

    def ready(self):
        import exchange.signals  # <-- Cette ligne charge ton signal au démarrage
