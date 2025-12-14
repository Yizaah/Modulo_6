from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('acceso-denegado/', views.acceso_denegado, name='acceso_denegado'),
    path('register/', views.register_view, name='register'),
]

