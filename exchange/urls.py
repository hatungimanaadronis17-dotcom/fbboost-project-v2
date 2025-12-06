from django.urls import path
from . import views

app_name = 'exchange'

urlpatterns = [
    path('', views.home, name='home'),
    path('gagner-coins/', views.gagner_coins, name='gagner_coins'),
    path('submit-task/', views.submit_task, name='submit_task'),
]
