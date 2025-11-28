# fbboost/middleware.py

from django.http import QueryDict
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class SafeNextRedirectMiddleware(MiddlewareMixin):
    """
    Protège contre les attaques par paramètre 'next' trop long ou en boucle infinie
    Exemple : ?next=/exchange/?next=/exchange/?next=...
    """

    def process_request(self, request):
        if request.method == "GET" and "next" in request.GET:
            next_value = request.GET.get("next", "")

            # Si le next est trop long ou contient trop de répétitions → on le supprime
            if len(next_value) > 500 or next_value.count("/exchange") > 5 or "next=" in next_value[50:]:
                logger.warning(f"Blocked dangerous 'next' parameter from {request.META.get('REMOTE_ADDR', 'unknown')} - Length: {len(next_value)}")

                # On recrée les paramètres GET sans le next dangereux
                mutable_get = request.GET.copy()
                mutable_get.pop("next", None)  # on enlève le next

                # On remplace request.GET par la version nettoyée
                request.GET = mutable_get

                # Optionnel : on peut aussi forcer un next propre
                if not request.user.is_authenticated:
                    request.GET = request.GET.copy()
                    request.GET["next"] = "/exchange/"
