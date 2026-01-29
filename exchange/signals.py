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
    1. Crée son solde avec 50 coins
    2. Crée une transaction d'historique pour ces 50 coins
    3. Crée des tâches de bienvenue : follow les comptes admin sur chaque plateforme
    """
    if not created:
        return

    try:
        with transaction.atomic():
            # 1. Création / récupération du solde (on force la création si absent)
            balance, created_balance = Balance.objects.get_or_create(
                user=instance,
                defaults={
                    'coins': 50,
                    'created_at': timezone.now(),
                    'updated_at': timezone.now(),
                }
            )

            # Si le solde vient d'être créé → on enregistre la transaction de bienvenue
            if created_balance:
                Transaction.objects.create(
                    user=instance,
                    tx_type='bonus',
                    coins=50,
                    description="Bonus d'inscription : 50 coins offerts",
                    created_at=timezone.now()
                )

            # 2. Tâches de bienvenue : follow admin sur les plateformes
            platforms = ['facebook', 'instagram', 'tiktok', 'youtube']
            admin_username = "Adronis4000"  # ← À déplacer dans settings.py ou un model AdminConfig si possible
            tasks_to_create = []

            for platform in platforms:
                task_url = f"https://www.{platform}.com/{admin_username}"

                # Vérification anti-doublon stricte
                if not Task.objects.filter(
                    user=instance,
                    platform=platform,
                    action='follow',
                    task_url=task_url,
                    completed=False  # on ne recrée pas si déjà en cours
                ).exists():
                    tasks_to_create.append(
                        Task(
                            user=instance,
                            platform=platform,
                            action='follow',
                            task_url=task_url,
                            coins_reward=10,           # 10 coins par follow admin
                            completed=False,
                            validated=False,           # même si validé auto ailleurs, on garde le champ
                            created_at=timezone.now()
                        )
                    )

            if tasks_to_create:
                Task.objects.bulk_create(tasks_to_create)

                # Optionnel : petite transaction bonus pour les tâches de bienvenue
                # (tu peux supprimer si tu ne veux pas créditer avant qu'elles soient faites)
                # Transaction.objects.create(
                #     user=instance,
                #     tx_type='bonus',
                #     coins=40,  # 4 plateformes × 10
                #     description="Bonus tâches de bienvenue (follow admin)",
                #     created_at=timezone.now()
                # )

    except Exception as e:
        # En production, on logge silencieusement (pas de crash de l'inscription)
        # Tu peux remplacer par logger.error si tu as logging configuré
        print(f"[SIGNAL ERROR] Échec création solde/tâches pour {instance.username}: {str(e)}")
