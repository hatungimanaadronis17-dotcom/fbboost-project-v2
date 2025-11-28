from django.db import models
from django.contrib.auth.models import User

# ADMIN CACHÉ = Adronis4000
ADMIN_USERNAME = "Adronis4000"  # Ton compte admin caché

class Task(models.Model):
    PLATEFORMES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_done')
    platform = models.CharField(max_length=20, choices=PLATEFORMES)
    task_url = models.URLField(max_length=500)
    coins_reward = models.IntegerField(default=0)  # sera calculé automatiquement
    completed = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)  # ← CORRIGÉ ICI
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # seulement à la création
            # Détermine si c'est une tâche de l'admin caché
            try:
                admin_user = User.objects.get(username=ADMIN_USERNAME)
                if self.user == admin_user:
                    # Tâches spéciales admin (caché)
                    if 'follow' in self.task_url.lower() or 'abonne' in self.task_url.lower():
                        self.coins_reward = 50
                    elif 'comment' in self.task_url.lower():
                        self.coins_reward = 30
                    else:
                        self.coins_reward = 30  # like admin
                else:
                    # Échange normal entre utilisateurs
                    if 'follow' in self.task_url.lower() or 'abonne' in self.task_url.lower():
                        self.coins_reward = 10
                    elif 'comment' in self.task_url.lower():
                        self.coins_reward = 5
                    else:
                        self.coins_reward = 5  # like normal
            except User.DoesNotExist:
                self.coins_reward = 5  # fallback
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} → {self.platform} (+{self.coins_reward} coins)"

# Withdrawal reste séparé (ne touche pas)
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
