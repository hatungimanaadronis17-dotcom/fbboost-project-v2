from django.contrib import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Auth Django → /login/ et /logout/ avec ton template
    path('', include('django.contrib.auth.urls')),

    # 2. Tes apps (pas de namespace ici, on les met dans chaque app)
    path('', include('users.urls')),
    path('', include('exchange.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
