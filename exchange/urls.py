app_name = 'exchange'
from django.urls import path,include
from . import views

urlpatterns = [
    path('', include('exchange.views.home'), name='home'),                    # page d'accueil (échange)
    path('submit/', views.submit_task, name='submit_task'),
    # Toutes tes autres URLs de l'espace échange ici
    # ex: path('task/<int:pk>/', views.task_detail, name='task_detail'),
]
