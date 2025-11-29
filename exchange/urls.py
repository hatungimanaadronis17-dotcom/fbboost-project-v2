from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                    # page d'accueil (échange)
    path('submit/', views.submit_task, name='submit_task'),
    # Toutes tes autres URLs de l'espace échange ici
    # ex: path('task/<int:pk>/', views.task_detail, name='task_detail'),
]
