from django.contrib import admin
from .models import Evento

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'ubicacion', 'autor')
    search_fields = ('nombre', 'descripcion', 'ubicacion')
    list_filter = ('fecha_inicio', 'fecha_fin', "ubicacion", "autor")
    ordering = ('-fecha_inicio',)
