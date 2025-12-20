from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_noop as _

# =========================
# CONSTANTES
# =========================

ADMIN_USERNAME = "Adronis4000"

PLATEFORMES = [
    ('facebook', _('Facebook')),
    ('instagram', _('Instagram')),
    ('tiktok', _('TikTok')),
    ('youtube', _('YouTube')),
]

ACTIONS = ['follow', 'subscribe', 'like', 'comment', 'abonne']
ACTION_CHOICES = [(a, a.capitalize()) for a in ACTIONS]

METHODES = [
    ('paypal', _('PayPal')),
    ('interac', _('Interac e-Transfer')),
    ('crypto', _('Crypto (USDT/BTC)')),
]

STATUS_CHOICES = [
    ('pending', _('Pending')),
    ('paid', _('Paid')),
]

# =========================
# MODELE BALANCE (CENTRAL)
# =========================

class Balance(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='balance'
    )
    coins = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} – {self.coins} coins"

# =========================
# MODELE TASK
# =========================

class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    platform = models.CharField(max_length=20, choices=PLATEFORMES)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    task_url = models.URLField(max_length=500)
    coins_reward = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Attribution automatique des récompenses
        (ne touche PAS à Balance ici, seulement à la task)
        """
        if not self.pk:
            try:
                admin_user = User.objects.get(username=ADMIN_USERNAME)

                # Si la task concerne l'admin
                if self.user == admin_user:
                    self.coins_reward = 50 if self.action in ['follow', 'subscribe', 'abonne'] else 30

                # Utilisateur normal
                else:
                    self.coins_reward = 10 if self.action in ['follow', 'subscribe', 'abonne'] else 5

            except User.DoesNotExist:
                self.coins_reward = 5

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} → {self.platform} ({self.action}) +{self.coins_reward} coins"

# =========================
# RETRAITS
# =========================

class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHODES)
    amount_cad = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount_cad} CAD ({self.status})"

# =========================
# LIENS ADMIN
# =========================

class ProfileLink(models.Model):
    platform = models.CharField(max_length=20, choices=PLATEFORMES)
    url = models.URLField(max_length=500)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform} → {self.url}"
