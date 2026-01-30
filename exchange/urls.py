# exchange/urls.py
from django.urls import path
from . import views

app_name = 'exchange'  # ← très bien, garde-le pour les reverse() et templates

urlpatterns = [
    # Page principale de l'échange (solde + liste tâches)
    path('', views.home, name='home'),

    # Soumission d'une tâche depuis le formulaire web (AJAX ou POST)
    path('submit/', views.submit_task, name='submit_task'),

    # Endpoint pour l'app Android (gagner coins via URL)
    path('gagner-coins/', views.gagner_coins, name='gagner_coins'),

    # Nouvelles URLs pour le flux de vérification automatique (timer 5s)
    path('task/<int:task_id>/', views.start_task, name='start_task'),
    path('task/<int:task_id>/confirm/', views.confirm_task, name='confirm_task'),
]
