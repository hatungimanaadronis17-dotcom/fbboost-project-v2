# users/urls.py

app_name = 'users'

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import TemplateView  # ← Ajouté pour une page d'accueil statique

urlpatterns = [
    # NOUVELLE LIGNE : Page d'accueil (chemin vide)
    path('', TemplateView.as_view(template_name='users/home.html'), name='home'),
    # OU si vous avez une vue personnalisée plus complexe :
    # path('', views.home, name='home'),

    # Vos URLs existantes
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    # Ajoute ici toutes les autres URLs de l'espace utilisateur
]
