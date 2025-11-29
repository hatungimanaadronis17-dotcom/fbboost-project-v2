from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Cette ligne fait marcher /login/ et /logout/ avec ton template
    path('', include('django.contrib.auth.urls')),

    # Tes deux apps (l’ordre n’a pas d’importance ici)
    path('', include('users.urls')),
    path('', include('exchange.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
