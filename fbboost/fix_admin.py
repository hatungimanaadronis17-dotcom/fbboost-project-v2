from django.contrib.auth.models import User

# Supprimer tous les utilisateurs
User.objects.all().delete()

# Recréer un superuser propre
User.objects.create_superuser(
    username="admin",
    email="hatungimanaadronis17@gmail.com",
    password="Admin1234!"
)

print("✔ Superuser admin recréé avec succès")
