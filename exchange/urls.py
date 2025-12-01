app_name = 'exchange'
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),                    # ← CORRIGÉ : views.home
    path('submit/', views.submit_task, name='submit_task'),
]
