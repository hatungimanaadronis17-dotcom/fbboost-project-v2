from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # App users → tout ce qui concerne login, register, profil, etc.
    path('', include('users.urls')),

    # App exchange → page d'accueil et tout le reste (échange, submit, etc.)
    path('', include('exchange.urls')),
]

# Media + static en développement (et Render accepte ça aussi en DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
