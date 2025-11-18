from django.db import models
from django.contrib.auth.models import User


class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    organizador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='eventos'
    )

    class Meta:
        permissions = [
            ("puede_editar_evento", "Puede editar evento"),
            ("puede_crear_evento", "Puede crear evento"),
        ]
        ordering = ['fecha']  # Opcional: ordena por fecha automáticamente

    def __str__(self):
        return self.nombre
