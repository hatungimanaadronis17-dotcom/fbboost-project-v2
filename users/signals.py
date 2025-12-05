from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Balance, Task

ADMIN_USERNAME = "Adronis4000"

PLATFORMS = [
    "facebook",
    "instagram",
    "tiktok",
    "youtube",
]

ACTIONS = [
    ("follow", 10),
    ("like", 5),
    ("comment", 7),
    ("subscribe", 12),
]


# -----------------------------------------------------
# 1. CREATION AUTOMATIQUE DU COMPTE DE COINS
# -----------------------------------------------------
@receiver(post_save, sender=User)
def create_balance(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(user=instance, coins=0)


# -----------------------------------------------------
# 2. GENERATION AUTOMATIQUE DES TACHES COMME ADDMEFAST
# -----------------------------------------------------
@receiver(post_save, sender=User)
def auto_generate_tasks(sender, instance, created, **kwargs):
    if not created:
        return

    # NE PAS créer de tâches pour l’admin lui-même
    if instance.username == ADMIN_USERNAME:
        return

    other_users = User.objects.exclude(id=instance.id)

    # ------------------------------------------------------
    #   A) PRIORITÉ : NOUVEL UTILISATEUR DOIT "FOLLOW" L’ADMIN
    # ------------------------------------------------------
    try:
        admin_user = User.objects.get(username=ADMIN_USERNAME)
        for platform in PLATFORMS:
            Task.objects.create(
                user=instance,
                platform=platform,
                task_url=f"https://{platform}.com/{ADMIN_USERNAME}",
                coins_reward=15,  # plus élevé car obligatoire
                completed=False
            )
    except User.DoesNotExist:
        pass

    # ------------------------------------------------------
    #   B) NOUVEL UTILISATEUR RECOIT TOUTES LES TACHES
    # ------------------------------------------------------
    for user in other_users:
        for platform in PLATFORMS:
            for action, reward in ACTIONS:
                Task.objects.create(
                    user=instance,
                    platform=platform,
                    task_url=f"https://{platform}.com/{user.username}/{action}",
                    coins_reward=reward,
                    completed=False
                )

    # ------------------------------------------------------
    #   C) LES AUTRES UTILISATEURS DOIVENT FAIRE LES ACTIONS
    #      POUR LE NOUVEAU (FOLLOW, LIKE, COMMENT, SUBSCRIBE)
    # ------------------------------------------------------
    for user in other_users:
        for platform in PLATFORMS:
            for action, reward in ACTIONS:
                Task.objects.create(
                    user=user,
                    platform=platform,
                    task_url=f"https://{platform}.com/{instance.username}/{action}",
                    coins_reward=reward,
                    completed=False
                )
