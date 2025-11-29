from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # AUTH DJANGO EN PREMIER – obligatoire pour que /login/ marche
    path('', include('django.contrib.auth.urls')),

    # Tes apps après
    path('', include('users.urls')),
    path('', include('exchange.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
