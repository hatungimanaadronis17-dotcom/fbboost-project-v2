# exchange/urls.py

from django.urls import path
from . import views

app_name = 'exchange'

urlpatterns = [
    # Page principale de l'échange (celle avec les boutons Facebook, TikTok, etc.)
    path('', views.home, name='home'),

    # URL appelée par le formulaire AJAX du site web
    path('submit/', views.submit_task, name='submit_task'),

    # URL pour l'app Android (si tu l'utilises toujours)
    path('gagner-coins/', views.gagner_coins, name='gagner_coins'),
]
