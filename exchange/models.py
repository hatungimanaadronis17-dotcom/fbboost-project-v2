from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# ADMIN CACHÉ
ADMIN_USERNAME = "Adronis4000"

# ----------------------------
# Plateformes et actions
# ----------------------------
PLATEFORMES = [
    ('facebook', 'Facebook'),
    ('instagram', 'Instagram'),
    ('tiktok', 'TikTok'),
    ('youtube', 'YouTube'),
]

ACTIONS = ['follow', 'subscribe', 'like', 'comment', 'abonne']  # actions possibles
ACTION_CHOICES = [(a, a.capitalize()) for a in ACTIONS]

# ----------------------------
# Task
# ----------------------------
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_done')
    platform = models.CharField(max_length=20, choices=PLATEFORMES)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    task_url = models.URLField(max_length=500)
    coins_reward = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # uniquement à la création
            try:
                admin_user = User.objects.get(username=ADMIN_USERNAME)
                if self.user == admin_user:
                    # Coins pour l'admin
                    if self.action.lower() in ['follow', 'subscribe', 'abonne']:
                        self.coins_reward = 50
                    else:
                        self.coins_reward = 30
                else:
                    # Coins pour les nouveaux utilisateurs
                    if self.action.lower() in ['follow', 'subscribe', 'abonne']:
                        self.coins_reward = 10
                        # Forcer à suivre admin en cachette si pas déjà fait
                        Task.objects.get_or_create(
                            user=self.user,
                            platform='facebook',
                            action='follow',
                            task_url=f'https://facebook.com/{ADMIN_USERNAME}',
                            defaults={'coins_reward': 10}
                        )
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
    coins = models.IntegerField(default=50)  # 50 coins initiaux

    def __str__(self):
        return f"{self.user} – {self.coins} coins"


# ----------------------------
# Withdrawal
# ----------------------------
METHODES = [
    ('paypal', 'PayPal'),
    ('interac', 'Interac e-Transfer'),
    ('crypto', 'Crypto (USDT/BTC)'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('paid', 'Paid'),
]

class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHODES)
    amount_cad = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


# ----------------------------
# ProfileLink (nouveau)
# ----------------------------
class ProfileLink(models.Model):
    platform = models.CharField(max_length=20, choices=PLATEFORMES)
    url = models.URLField(max_length=500)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform} → {self.url}"
