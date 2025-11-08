from django.contrib import admin
from .models import Recipe, ContactMessage
from django.utils.html import format_html
from django.templatetags.static import static


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
	# Mostrar el alias `nombre` (no disruptivo) en lugar de `title` para mayor claridad
	list_display = ('nombre', 'created_at', 'image_tag')
	prepopulated_fields = {'slug': ('title',)}

	def image_tag(self, obj):
		if obj.image:
			# small square thumbnail with cover crop to keep consistency
			return format_html('<img src="{}" style="height:60px; width:60px; object-fit:cover; border-radius:6px;" class="admin-image-thumb"/>', static(obj.image))
		return "-"

	image_tag.short_description = 'Imagen'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'subject', 'created_at')
	readonly_fields = ('created_at',)
