from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ProfileLink, Task, Balance, ADMIN_USERNAME, ACTIONS

@receiver(post_save, sender=ProfileLink)
def create_tasks_for_users(sender, instance, created, **kwargs):
    """
    Lorsqu'un nouveau ProfileLink est ajouté, créer automatiquement
    une task pour tous les utilisateurs (sauf l'admin lui-même)
    pour toutes les actions définies dans ACTIONS.
    """
    if created:
        users = User.objects.exclude(username=ADMIN_USERNAME)
        for user in users:
            for action in ACTIONS:
                # Vérifie si la task existe déjà
                task_exists = Task.objects.filter(
                    user=user,
                    platform=instance.platform,
                    task_url=instance.url,
                    action=action
                ).exists()
                if not task_exists:
                    coins_reward = 10 if action in ['follow', 'subscribe', 'abonne'] else 5
                    Task.objects.create(
                        user=user,
                        platform=instance.platform,
                        action=action,
                        task_url=instance.url,
                        coins_reward=coins_reward
                    )

@receiver(post_save, sender=User)
def create_balance_and_tasks_for_new_user(sender, instance, created, **kwargs):
    """
    Lorsqu'un nouvel utilisateur est créé :
    - Créer un solde initial de 50 coins
    - Créer des tasks forcées pour suivre/like/comment les liens admin
    """
    if created:
        # Crée balance initiale
        Balance.objects.create(user=instance, coins=50)

        # Crée les tasks forcées pour suivre l'admin
        try:
            admin_user = User.objects.get(username=ADMIN_USERNAME)
            # Tu peux ajouter toutes les plateformes où l'admin est présent
            platforms = ['facebook', 'instagram', 'tiktok', 'youtube']
            for platform in platforms:
                Task.objects.get_or_create(
                    user=instance,
                    platform=platform,
                    action='follow',
                    task_url=f'https://{platform}.com/{ADMIN_USERNAME}',
                    defaults={'coins_reward': 10}
                )
        except User.DoesNotExist:
            pass
