# exchange/urls.py

from django.urls import path
from . import views

app_name = 'exchange'

urlpatterns = [
    # Page principale de l'échange
    path('', views.home, name='home'),

    # Soumission AJAX du site web
    path('submit/', views.submit_task, name='submit_task'),

    # Pour l'app Android
    path('gagner-coins/', views.gagner_coins, name='gagner_coins'),
]
