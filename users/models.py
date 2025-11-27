from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auto_boost = models.BooleanField(default=True)
    boost_delay = models.IntegerField(default=30)  # secondes

    def __str__(self):
        return f"{self.user.username}'s profile"
