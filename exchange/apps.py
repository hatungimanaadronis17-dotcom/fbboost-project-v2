# exchange/apps.py
from django.apps import AppConfig


class ExchangeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exchange'

    def ready(self):
        # Cette ligne charge les signals définis dans signals.py
        import exchange.signals  # noqa: F401
