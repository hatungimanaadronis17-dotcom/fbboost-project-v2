from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentification Django (login, logout, password reset…)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Tes applications
    path('', include('users.urls')),       # page d'accueil, profil, etc.
    path('', include('exchange.urls')),    # ici vont aller toutes les routes de boost
]

# Servir les médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
