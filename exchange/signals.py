from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.apps import apps

from .models import ADMIN_USERNAME, ACTIONS


def get_models():
    ProfileLink = apps.get_model('exchange', 'ProfileLink')
    Task = apps.get_model('exchange', 'Task')
    Balance = apps.get_model('exchange', 'Balance')
    return ProfileLink, Task, Balance


# ==================================================
# 1️⃣ Création automatique des tasks pour tous
#    quand un lien admin est ajouté
# ==================================================

@receiver(post_save)
def create_tasks_for_users(sender, instance, created, **kwargs):
    ProfileLink, Task, Balance = get_models()

    if sender != ProfileLink or not created:
        return

    users = User.objects.exclude(username=ADMIN_USERNAME)
    tasks_to_create = []

    for user in users:
        for action in ACTIONS:
            exists = Task.objects.filter(
                user=user,
                platform=instance.platform,
                task_url=instance.url,
                action=action
            ).exists()

            if not exists:
                coins_reward = 10 if action in ['follow', 'subscribe', 'abonne'] else 5
                tasks_to_create.append(
                    Task(
                        user=user,
                        platform=instance.platform,
                        action=action,
                        task_url=instance.url,
                        coins_reward=coins_reward
                    )
                )

    if tasks_to_create:
        Task.objects.bulk_create(tasks_to_create)


# ==================================================
# 2️⃣ Création du Balance + tasks de bienvenue
#    à l'inscription
# ==================================================

@receiver(post_save, sender=User)
def create_balance_and_tasks_for_new_user(sender, instance, created, **kwargs):
    if not created:
        return

    ProfileLink, Task, Balance = get_models()

    # --- Balance initial ---
    Balance.objects.get_or_create(
        user=instance,
        defaults={'coins': 50}
    )

    platforms = ['facebook', 'instagram', 'tiktok', 'youtube']
    tasks_to_create = []

    for platform in platforms:
        task_url = f'https://www.{platform}.com/{ADMIN_USERNAME}'

        exists = Task.objects.filter(
            user=instance,
            platform=platform,
            action='follow',
            task_url=task_url
        ).exists()

        if not exists:
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
