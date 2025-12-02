from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField() 
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    ubicacion = models.CharField(max_length=300)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.nombre