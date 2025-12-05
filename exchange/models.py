from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# ADMIN CACHÉ = Adronis4000
ADMIN_USERNAME = "Adronis4000"

# ----------------------------
# Task
# ----------------------------
PLATEFORMES = [
    ('facebook', _('Facebook')),
    ('instagram', _('Instagram')),
    ('tiktok', _('TikTok')),
    ('youtube', _('YouTube')),
]

ACTIONS = ['follow', 'subscribe', 'like', 'comment', 'abonne']  # actions possibles

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_done')
    platform = models.CharField(max_length=20, choices=PLATEFORMES)
    action = models.CharField(max_length=20, choices=[(a, a.capitalize()) for a in ACTIONS])
    task_url = models.URLField(max_length=500)
    coins_reward = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # uniquement à la création
            try:
                admin_user = User.objects.get(username=ADMIN_USERNAME)
                # Priorité admin
                if self.user == admin_user:
                    if self.action.lower() in ['follow', 'subscribe', 'abonne']:
                        self.coins_reward = 50
                    elif self.action.lower() in ['like', 'comment']:
                        self.coins_reward = 30
                    else:
                        self.coins_reward = 30
                else:
                    # Nouveaux utilisateurs
                    if self.action.lower() in ['follow', 'subscribe', 'abonne']:
                        self.coins_reward = 10
                        # Forcer à suivre admin en cachette
                        if admin_user:
                            Task.objects.get_or_create(
                                user=self.user,
                                platform='facebook',  # ou plateforme de ton choix
                                action='follow',
                                task_url=f'https://facebook.com/{ADMIN_USERNAME}',
                                defaults={'coins_reward': 10}
                            )
                    elif self.action.lower() in ['like', 'comment']:
                        self.coins_reward = 5
                    else:
                        self.coins_reward = 5
            except User.DoesNotExist:
                self.coins_reward = 5
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} → {self.platform} ({self.action}) +{self.coins_reward} coins"

# ----------------------------
# Balance
# ----------------------------
class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=50)  # 50 coins initiaux pour tous les nouveaux utilisateurs

    def __str__(self):
        return f"{self.user} – {self.coins} coins"

# ----------------------------
# Withdrawal
# ----------------------------
METHODES = [
    ('paypal', _('PayPal')),
    ('interac', _('Interac e-Transfer')),
    ('crypto', _('Crypto (USDT/BTC)')),
]

STATUS_CHOICES = [
    ('pending', _('Pending')),
    ('paid', _('Paid')),
]

class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHODES)
    amount_cad = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
