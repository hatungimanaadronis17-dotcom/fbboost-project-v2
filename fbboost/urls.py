from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),                      # Admin Django → fonctionne
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password… sur /accounts/login/
    path('users/', include('users.urls')),                # tes vues personnalisées users
    path('', include('exchange.urls')),                   # tout le reste (page d’accueil, etc.)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
