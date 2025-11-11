from django.contrib import admin

# admin.py

from django.contrib import admin
from .models import Event, Participant # 1. Importa tus modelos

# 2. Registra el modelo Event
# Esto hace que aparezca en el panel de administración
admin.site.register(Event) 

# 3. Registra el modelo Participant
# Esto hace que también aparezca para ver los detalles
admin.site.register(Participant)

# Register your models here.
