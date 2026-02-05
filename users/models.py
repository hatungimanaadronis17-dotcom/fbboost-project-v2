from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserSecurity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(
        default=timezone.now,          # ← remplace auto_now_add par ça
        verbose_name="Créé le"
    )

    def __str__(self):
        return self.user.username
