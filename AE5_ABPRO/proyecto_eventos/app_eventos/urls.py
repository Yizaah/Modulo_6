from django.urls import path
from django.views.generic import RedirectView
from .views import ListaEventos, MisEventos
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', ListaEventos.as_view(), name='lista_eventos'),

    # Alias opcional para evitar el error 404 del admin
    path('lista-eventos/', RedirectView.as_view(url='/', permanent=False)),

    path('mis_eventos/', MisEventos.as_view(), name='mis_eventos'),

    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="lista_eventos"), name="logout"),
]