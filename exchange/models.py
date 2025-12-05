from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_noop as _

ADMIN_USERNAME = "Adronis4000"

PLATEFORMES = [
    ('facebook', _('Facebook')),
    ('instagram', _('Instagram')),
    ('tiktok', _('TikTok')),
    ('youtube', _('YouTube')),
]

ACTIONS = ['follow', 'subscribe', 'like', 'comment', 'abonne']
ACTION_CHOICES = [(a, a.capitalize()) for a in ACTIONS]


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
        if not self.pk:
            try:
                admin_user = User.objects.get(username=ADMIN_USERNAME)
                if self.user == admin_user:
                    if self.action.lower() in ['follow', 'subscribe', 'abonne']:
                        self.coins_reward = 50
                    else:
                        self.coins_reward = 30
                else:
                    if self.action.lower() in ['follow', 'subscribe', 'abonne']:
                        self.coins_reward = 10
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


class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=50)

    def __str__(self):
        return f"{self.user} – {self.coins} coins"


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


class ProfileLink(models.Model):
    platform = models.CharField(max_length=20, choices=PLATEFORMES)
    url = models.URLField(max_length=500)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform} → {self.url}"
