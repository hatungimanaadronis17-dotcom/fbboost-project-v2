from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Import correct selon ton dernier code
from exchange.models import Balance, Task, ADMIN_USERNAME

@receiver(post_save, sender=User)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        # Crée automatiquement le balance
        Balance.objects.create(user=instance, coins=50)

        # Forcer à suivre admin en priorité
        try:
            admin_user = User.objects.get(username=ADMIN_USERNAME)
            if admin_user:
                Task.objects.get_or_create(
                    user=instance,
                    platform='facebook',  # ajuster selon plateforme si besoin
                    task_url=f'https://facebook.com/{ADMIN_USERNAME}',
                    defaults={'coins_reward': 10}
                )
        except User.DoesNotExist:
            pass
