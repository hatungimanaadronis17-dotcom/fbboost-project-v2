from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # --- TES CHAMPS ORIGINAUX ---
    auto_boost = models.BooleanField(default=True)
    boost_delay = models.IntegerField(default=30)  # secondes

    # --- CHAMPS IMPORTANTS (point 3 que tu voulais ajouter) ---
    coins = models.IntegerField(default=0)
    boosts = models.IntegerField(default=0)

    # --- CHAMP UTILE (ne casse rien) ---
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            coins=50,     # 🎁 bonus inscription
            boosts=0
        )
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
