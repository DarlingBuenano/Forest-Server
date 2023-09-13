from django.urls import path
from api_restful import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('nombre-modelo/', views.nombre_modelo, name="nombre-modelo"),
    path('procesar-foto/', views.procesarFoto, name="procesar-foto"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)