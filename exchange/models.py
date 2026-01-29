from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User


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
# BALANCE / WALLET (table: exchange_balance)
# =========================
class Balance(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='balance',
        verbose_name=_("Utilisateur")
    )
    coins = models.PositiveIntegerField(
        default=50,  # ← 50 coins offerts à la création
        verbose_name=_("Coins")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Créé le")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Mis à jour le")
    )

    class Meta:
        verbose_name = _("Solde")
        verbose_name_plural = _("Soldes")
        ordering = ['-created_at']
        # db_table = 'exchange_balance'   # ← optionnel, Django le fait déjà automatiquement

    def __str__(self):
        return f"{self.user.username} – {self.coins} coins"


# =========================
# TRANSACTIONS (historique)
# =========================
class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name=_("Utilisateur")
    )
    tx_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
        verbose_name=_("Type")
    )
    coins = models.IntegerField(verbose_name=_("Coins"))
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
# TASKS (tâches à accomplir)
# =========================
class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_("Utilisateur")
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
            return False

        with transaction.atomic():
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
        related_name='withdrawals',
        verbose_name=_("Utilisateur")
    )
    method = models.CharField(
        max_length=20,
        choices=METHODES,
        verbose_name=_("Méthode")
    )
    coins_amount = models.PositiveIntegerField(verbose_name=_("Montant en coins"))
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
        if self.pk is None:  # seulement à la création
            self.amount_cad = self.coins_amount / COINS_TO_CAD_RATE
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} – {self.coins_amount} coins → {self.amount_cad}$ CAD ({self.status})"


# =========================
# SIGNAL : Création auto du solde à 50 coins lors de l'inscription
# =========================
@receiver(post_save, sender=User)
def create_user_balance(sender, instance, created, **kwargs):
    """
    Crée automatiquement un objet Balance avec 50 coins
    quand un nouvel utilisateur est créé.
    """
    if created:
        Balance.objects.create(user=instance)
        # Optionnel : pour debug dans la console Termux
        print(f"[SIGNAL] → Solde créé avec 50 coins pour {instance.username}")
