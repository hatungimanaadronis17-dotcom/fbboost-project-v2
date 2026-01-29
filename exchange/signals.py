# exchange/signals.py
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Balance, Transaction, Task


@receiver(post_save, sender=User)
def create_balance_and_welcome_tasks(sender, instance, created, **kwargs):
    """
    À la création d'un nouvel utilisateur :
    - Crée le solde avec 50 coins
    - Enregistre la transaction bonus
    - Crée les tâches de bienvenue (follow admin sur chaque plateforme)
    """
    if not created:
        return

    try:
        with transaction.atomic():
            # Création du solde (50 coins par défaut)
            balance, created_balance = Balance.objects.get_or_create(
                user=instance,
                defaults={
                    'coins': 50,
                    'created_at': timezone.now(),
                    'updated_at': timezone.now(),
                }
            )

            # Transaction historique pour les 50 coins d'inscription
            if created_balance:
                Transaction.objects.create(
                    user=instance,
                    tx_type='bonus',
                    coins=50,
                    description="Bonus d'inscription : 50 coins offerts",
                    created_at=timezone.now()
                )

            # Tâches de bienvenue : follow des comptes admin
            platforms = ['facebook', 'instagram', 'tiktok', 'youtube']
            admin_username = "Adronis4000"  # ← À déplacer dans settings.py plus tard (ex: settings.ADMIN_SOCIAL_USERNAME)
            tasks_to_create = []

            for platform in platforms:
                task_url = f"https://www.{platform}.com/{admin_username}"

                # Anti-doublon : on ne recrée pas si tâche déjà existante (même incomplète)
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
                            coins_reward=10,              # 10 coins par follow
                            completed=False,
                            validated=False,              # même si validé auto plus tard
                            created_at=timezone.now()
                        )
                    )

            if tasks_to_create:
                Task.objects.bulk_create(tasks_to_create)

                # Optionnel : tu peux ici créditer les 40 coins immédiatement si tu considères
                # que suivre l'admin est "garanti" ou "motivationnel" → sinon laisse commenté
                # Transaction.objects.create(
                #     user=instance,
                #     tx_type='bonus',
                #     coins=40,
                #     description="Bonus tâches bienvenue (follow admin sur 4 plateformes)",
                #     created_at=timezone.now()
                # )

    except Exception as e:
        # En cas d'erreur : on ne fait pas planter l'inscription
        # Tu peux remplacer par un vrai logger plus tard
        print(f"[SIGNAL ERROR] Problème lors de la création solde/tâches pour {instance.username}: {e}")
