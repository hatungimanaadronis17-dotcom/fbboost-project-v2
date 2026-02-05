# users/models.py

from django.db import models
from django.conf import settings

class UserSecurity(models.Model):
    # Lien avec le modèle utilisateur de Django
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Exemple de champs pour sécurité
    security_question = models.CharField(max_length=255)
    security_answer = models.CharField(max_length=255)

    # Champs de date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Security Info"
