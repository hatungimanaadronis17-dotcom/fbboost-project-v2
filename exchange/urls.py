from django.urls import path
from . import views

app_name = 'exchange'

urlpatterns = [
    path('gagner-coins/', views.gagner_coins, name='gagner_coins'),
    path('task/', views.task, name='task'),                           # optionnel
    path('complete/', views.complete_task, name='complete_task'),     # optionnel
    path('add-task/', views.add_task, name='add_task'),               # si tu veux poster des tâches
]
