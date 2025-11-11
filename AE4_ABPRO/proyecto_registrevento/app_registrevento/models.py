from django.db import models

# Create your models here.


class Event(models.Model):
	nombre = models.CharField(max_length=100)
	fecha = models.DateField()
	ubicacion = models.CharField(max_length=200, blank=True)

	def __str__(self) -> str:
		return f"{self.nombre} - {self.fecha}"


class Participant(models.Model):
	event = models.ForeignKey(Event, related_name='participantes', on_delete=models.CASCADE)
	nombre = models.CharField(max_length=100)
	correo = models.EmailField()

	def __str__(self) -> str:
		return f"{self.nombre} <{self.correo}> ({self.event.nombre})"
