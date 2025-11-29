from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth Django en premier (pour que /login/ marche sans conflit)
    path('', include('django.contrib.auth.urls')),

    # Tes apps avec NAMESPACE explicite (c'est ÇA qui fixe le KeyError 'exchange')
    path('', include('users.urls', namespace='users')),
    path('', include('exchange.urls', namespace='exchange')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
