from django.urls import path
from . import views

app_name = 'exchange'

urlpatterns = [
    path('', views.exchange_home, name='home'),
    path('submit/', views.submit_task, name='submit_task'),
]
