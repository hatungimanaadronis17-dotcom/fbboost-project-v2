from django.db import models
from django.contrib.auth.models import User

class UserSecurity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(
        default="0.0.0.0",  # valeur temporaire valide pour les anciennes lignes
    )
    user_agent = models.TextField(
        default="",         # ajoute aussi un default si c'est non-nullable et nouveau
    )
    created_at = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.user.username
