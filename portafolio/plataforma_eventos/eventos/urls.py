from django.urls import path
from .views import (
    home,
    EventoListView,
    EventoCreateView,
    EventoUpdateView,
    EventoDeleteView,
    EventoDetailView,
    register,
    register_done,
    activate,
    acceso_denegado,
)

urlpatterns = [
    path('', home, name='home'),

    path('eventos/', EventoListView.as_view(), name='evento_list'),
    path('eventos/crear/', EventoCreateView.as_view(), name='evento_create'),
    path('eventos/<int:pk>/', EventoDetailView.as_view(), name='evento_detail'),
    path('eventos/<int:pk>/editar/', EventoUpdateView.as_view(), name='evento_update'),
    path('eventos/<int:pk>/eliminar/', EventoDeleteView.as_view(), name='evento_delete'),
    path('register/', register, name='register'),
    path('register/done/', register_done, name='register_done'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('acceso_denegado/', acceso_denegado, name='acceso_denegado'),
]
