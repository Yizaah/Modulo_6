from django.db import models
from django.utils.text import slugify


class Recipe(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True, blank=True)
	short_description = models.CharField(max_length=255, blank=True)
	# Ruta relativa dentro de la carpeta static, por ejemplo: 'images/mi_receta.jpg'
	image = models.CharField(max_length=255, blank=True, help_text="Ruta relativa en static, ej. 'images/miimagen.jpg'")
	ingredients = models.TextField()
	instructions = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title

	# Non-disruptive Spanish aliases to keep compatibility with requests
	@property
	def nombre(self):
		"""Alias no disruptivo para `title` (nombre de la receta)."""
		return self.title

	@property
	def imagen(self):
		"""Alias no disruptivo para `image` (ruta relativa en static)."""
		return self.image


class ContactMessage(models.Model):
	name = models.CharField(max_length=120)
	email = models.EmailField()
	subject = models.CharField(max_length=200)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.name} - {self.subject}"
