from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from users.models import Balance
from exchange.models import Task, ADMIN_USERNAME

# ----------------------------
# Création automatique du Balance à l'inscription
# ----------------------------
@receiver(post_save, sender=User)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        # Crée le balance avec 50 coins initiaux
        Balance.objects.create(user=instance, coins=50)

        # Forcer le nouvel utilisateur à suivre l'admin en priorité
        try:
            admin_user = User.objects.get(username=ADMIN_USERNAME)
            if admin_user:
                Task.objects.get_or_create(
                    user=instance,
                    platform='facebook',  # ou autre plateforme si tu veux
                    action='follow',
                    task_url=f'https://facebook.com/{ADMIN_USERNAME}',
                    defaults={'coins_reward': 10}
                )
        except User.DoesNotExist:
            pass
