# exchange/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Balance, Task  # Import direct, plus besoin de get_models()

@receiver(post_save, sender=User)
def create_balance_and_welcome_tasks(sender, instance, created, **kwargs):
    if not created:
        return

    # Création du Balance avec 50 coins de bienvenue
    Balance.objects.get_or_create(
        user=instance,
        defaults={'coins': 50}
    )

    # Tasks de bienvenue : follow les comptes admin sur chaque plateforme
    platforms = ['facebook', 'instagram', 'tiktok', 'youtube']
    admin_username = "Adronis4000"  # Tu peux aussi l'importer depuis models si tu veux
    tasks_to_create = []

    for platform in platforms:
        task_url = f'https://www.{platform}.com/{admin_username}'

        # Évite les doublons
        if not Task.objects.filter(
            user=instance,
            platform=platform,
            action='follow',
            task_url=task_url
        ).exists():
            tasks_to_create.append(
                Task(
                    user=instance,
                    platform=platform,
                    action='follow',
                    task_url=task_url,
                    coins_reward=10
                )
            )

    if tasks_to_create:
        Task.objects.bulk_create(tasks_to_create)
