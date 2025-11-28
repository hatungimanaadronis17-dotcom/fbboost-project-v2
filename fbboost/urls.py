from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('exchange/', include('exchange.urls')),
    path('', include('exchange.urls')),  # page d'accueil = échange
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', include('users.urls')),  # inscription
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
