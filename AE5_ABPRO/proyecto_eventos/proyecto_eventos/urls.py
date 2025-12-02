from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Tu app principal
    path('', include("app_eventos.urls")),

    # TODAS las rutas de login/logout de Django
    path('', include("django.contrib.auth.urls")),
]