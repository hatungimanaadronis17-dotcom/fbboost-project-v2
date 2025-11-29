from django.urls import path
from django.contrib.auth import views as auth_views
from . import views   # ← remplace par tes vraies vues si tu en as des personnalisées

urlpatterns = [
    # Login / Logout (tu peux garder les vues Django ou les remplacer par les tiennes)
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Inscription
    path('register/', views.register, name='register'),              # ← ta vue register
    path('profile/', views.profile, name='profile'),                 # ← ta vue profil (si tu en as une)
    # Ajoute ici toutes les autres URLs de l'espace utilisateur
]
