from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# =========================
# PROFILE
# =========================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # --- Paramètres utilisateur ---
    auto_boost = models.BooleanField(default=True)
    boost_delay = models.IntegerField(default=30)  # secondes

    # --- Utilitaire ---
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


# =========================
# SIGNAL : création automatique du profile
# =========================
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
