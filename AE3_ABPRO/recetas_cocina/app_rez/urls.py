from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contacto/', views.contacto, name='contacto'),
    path('contacto/enviado/', views.contacto_ok, name='contacto_ok'),
    path('recetas/', views.recetas, name='recetas'),
    path('recetas/<slug:slug>/', views.receta_detail, name='receta_detail'),
]