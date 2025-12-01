# users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # On ne fait la création du profil QUE si l’utilisateur vient d’être créé
    # ET si le profil n’existe pas déjà (protection contre les doublons)
    if created:
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # On sauvegarde le profil seulement s’il existe déjà
    # (évite l’erreur "profile does not exist" quand on crée le superuser)
    if hasattr(instance, 'profile'):
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            # Si jamais il manque (cas très rare), on le crée
            Profile.objects.create(user=instance)
