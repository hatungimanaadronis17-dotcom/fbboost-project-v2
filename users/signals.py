from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import transaction
from django.db.utils import OperationalError

from exchange.models import Balance, Transaction
from users.models import UserSecurity


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        with transaction.atomic():
            Balance.objects.create(user=instance, coins=50)
            Transaction.objects.create(
                user=instance,
                tx_type='bonus',
                coins=50,
                description="Bonus inscription"
            )
    except OperationalError:
        pass
