app_name = 'exchange'
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.exchange_home, name='home'),          # ← CORRIGÉ
    path('submit/', views.submit_task, name='submit_task'),
]
