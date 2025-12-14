from django.contrib import admin
from .models import Evento

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'fecha', 'es_privado', 'organizador')
    list_filter = ('tipo', 'es_privado')
    search_fields = ('titulo',)
