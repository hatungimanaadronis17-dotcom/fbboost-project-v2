from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# =========================
# CONSTANTES
# =========================

ADMIN_USERNAME = "Adronis4000"
COINS_TO_CAD_RATE = 100  # 100 coins = 1 CAD

PLATEFORMES = [
    ('facebook', _('Facebook')),
    ('instagram', _('Instagram')),
    ('tiktok', _('TikTok')),
    ('youtube', _('YouTube')),
]

ACTIONS = ['follow', 'subscribe', 'like', 'comment', 'abonne']
ACTION_CHOICES = [(a, _(a.capitalize())) for a in ACTIONS]

METHODES = [
    ('paypal', _('PayPal')),
    ('interac', _('Interac e-Transfer')),
    ('crypto', _('Crypto')),
]

STATUS_CHOICES = [
    ('pending', _('Pending')),
    ('paid', _('Paid')),
    ('rejected', _('Rejected')),
]

TRANSACTION_TYPES = [
    ('credit', _('Credit')),
    ('debit', _('Debit')),
    ('withdrawal', _('Withdrawal')),
    ('bonus', _('Bonus')),
]

# =========================
# BALANCE / WALLET
# =========================

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    coins = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def coins_to_cad(self):
        return self.coins / COINS_TO_CAD_RATE

    def __str__(self):
        return f"{self.user.username} - {self.coins} coins"


# =========================
# TRANSACTIONS
# =========================

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    tx_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    coins = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} | {self.tx_type} | {self.coins} coins"


# =========================
# TASKS
# =========================

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    platform = models.CharField(max_length=20, choices=PLATEFORMES)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    task_url = models.URLField(max_length=500)
    coins_reward = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def validate(self):
        if self.validated:
            return

        with transaction.atomic():
            balance = self.user.balance
            balance.coins += self.coins_reward
            balance.save()

            Transaction.objects.create(
                user=self.user,
                tx_type='credit',
                coins=self.coins_reward,
                description=f"Reward task {self.platform}"
            )

            self.validated = True
            self.save()

    def __str__(self):
        return f"{self.user.username} → {self.platform} +{self.coins_reward}"


# =========================
# WITHDRAWAL
# =========================

class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHODES)
    coins_amount = models.PositiveIntegerField()
    amount_cad = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.amount_cad:
            self.amount_cad = self.coins_amount / COINS_TO_CAD_RATE
        super().save(*args, **kwargs)
