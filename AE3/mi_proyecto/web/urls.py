from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('', views.pagina_estatica, name='pagina_estatica'),
]