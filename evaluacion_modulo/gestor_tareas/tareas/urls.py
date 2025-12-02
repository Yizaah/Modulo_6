from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tareas, name='lista_tareas'),
    path('detalle/<int:id>/', views.detalle_tarea, name='detalle_tarea'),
    path('agregar/', views.agregar_tarea, name='agregar_tarea'),
    path('eliminar/<int:id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('signup/', views.signup, name='signup'),
]