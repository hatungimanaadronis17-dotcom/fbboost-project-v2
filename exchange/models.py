from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PLATEFORMES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATEFORMES)
    task_url = models.URLField()
    coins_reward = models.IntegerField(default=10)
    completed = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.platform}"

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)

class Withdrawal(models.Model):
    METHODES = [
        ('paypal', 'PayPal'),
        ('interac', 'Interac e-Transfer'),
        ('crypto', 'Crypto (USDT/BTC)'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHODES)
    amount_cad = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.CharField(max_length=200)  # email PayPal ou wallet crypto
    status = models.CharField(max_length=20, default='pending')  # pending, paid, rejected
    created_at = models.DateTimeField(auto_now_add=True)
