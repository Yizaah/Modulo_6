from django.urls import path
from . import views
app_name = 'mi_aplicacion'
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path("index", views.index, name="index")
    #path('dato/<str:valor>/', views.recibir_dato, name='recibir_dato'),
]