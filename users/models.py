from django.utils import timezone

class UserSecurity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)  # <-- ajoute default
    updated_at = models.DateTimeField(auto_now=True)
