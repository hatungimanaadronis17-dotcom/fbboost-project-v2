from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# =========================
# CONSTANTES
# =========================
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
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='balance'          # ← important pour request.user.balance
    )
    coins = models.PositiveIntegerField(
        default=50,                     # 50 coins gratuits à l'inscription
        verbose_name=_("Coins")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Balance")
        verbose_name_plural = _("Balances")

    def __str__(self):
        return f"{self.user.username} – {self.coins} coins"


# =========================
# TRANSACTIONS (historique)
# =========================
class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    tx_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
        verbose_name=_("Type")
    )
    coins = models.IntegerField(
        verbose_name=_("Coins")
    )  # Peut être négatif pour les débits/retraits
    description = models.CharField(
        max_length=255,
        verbose_name=_("Description")
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Date")
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    def __str__(self):
        sign = "+" if self.coins > 0 else ""
        return f"{self.user.username} | {self.tx_type} | {sign}{self.coins} coins"


# =========================
# TASKS
# =========================
class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    platform = models.CharField(
        max_length=20,
        choices=PLATEFORMES,
        verbose_name=_("Plateforme")
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name=_("Action")
    )
    task_url = models.URLField(
        max_length=500,
        verbose_name=_("Lien de la tâche")
    )
    coins_reward = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Récompense (coins)")
    )
    completed = models.BooleanField(
        default=False,
        verbose_name=_("Complétée par l'utilisateur")
    )
    validated = models.BooleanField(
        default=False,
        verbose_name=_("Validée par admin")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Créée le")
    )
    validated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Validée le")
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Tâche")
        verbose_name_plural = _("Tâches")

    def validate_reward(self):
        """Valide la tâche et crédite les coins (idempotent)"""
        if self.validated:
            return False  # déjà validée

        with transaction.atomic():
            # On recharge l'objet pour éviter les race conditions
            balance = Balance.objects.select_for_update().get(user=self.user)

            balance.coins += self.coins_reward
            balance.save(update_fields=['coins', 'updated_at'])

            Transaction.objects.create(
                user=self.user,
                tx_type='credit',
                coins=self.coins_reward,
                description=f"Reward validated: {self.platform} - {self.action}"
            )

            self.validated = True
            self.validated_at = timezone.now()
            self.save(update_fields=['validated', 'validated_at'])

        return True

    def __str__(self):
        status = "✓" if self.validated else "⌛" if self.completed else "⏳"
        return f"{self.user.username} → {self.platform} {self.action} {status} +{self.coins_reward}"


# =========================
# RETRAIT (WITHDRAWAL)
# =========================
class Withdrawal(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='withdrawals'
    )
    method = models.CharField(
        max_length=20,
        choices=METHODES,
        verbose_name=_("Méthode")
    )
    coins_amount = models.PositiveIntegerField(
        verbose_name=_("Montant en coins")
    )
    amount_cad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Montant CAD")
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_("Statut")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Demandé le")
    )
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Traité le")
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Retrait")
        verbose_name_plural = _("Retraits")

    def save(self, *args, **kwargs):
        if self.pk is None:  # Création uniquement
            # Conversion automatique seulement à la création
            self.amount_cad = self.coins_amount / COINS_TO_CAD_RATE
            # On peut aussi ajouter ici une vérification : self.coins_amount >= MIN_WITHDRAWAL
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} – {self.coins_amount} coins → {self.amount_cad}$ CAD ({self.status})"
