from django.core.management.base import BaseCommand
from exchange.models import Withdrawal

class Command(BaseCommand):
    def handle(self, *args, **options):
        Withdrawal.objects.create(
            user_id=1,  # ton compte admin
            method='interac',
            amount_cad=5000,
            details='Hatungimanaadronis17@gmail.com',
            status='paid'
        )
        self.stdout.write("5000 $CAD retirés avec succès (Interac)")
