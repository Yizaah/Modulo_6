from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('acceso-denegado/', views.acceso_denegado, name='acceso_denegado'),

    # Eventos
    path('eventos/', views.ListaEventosView.as_view(), name='lista_eventos'),
    path('eventos/crear/', views.CrearEventoView.as_view(), name='crear_evento'),
    path('eventos/editar/<int:pk>/', views.EditarEventoView.as_view(), name='editar_evento'),
    path('eventos/eliminar/<int:pk>/', views.EliminarEventoView.as_view(), name='eliminar_evento'),
]