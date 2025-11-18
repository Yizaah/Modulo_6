# app_gestion/signals.py
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Evento


@receiver(post_migrate)
def crear_grupos_y_permisos(sender, **kwargs):
    # Solo ejecutar esto cuando se migra la app_gestion
    if sender.name != 'app_gestion':
        return

    content_type = ContentType.objects.get_for_model(Evento)

    # Crear grupos si no existen
    admin_group, _ = Group.objects.get_or_create(name='Administradores')
    organizador_group, _ = Group.objects.get_or_create(name='Organizadores')
    asistente_group, _ = Group.objects.get_or_create(name='Asistentes')

    # Crear los permisos personalizados si no existen
    Permission.objects.get_or_create(
        codename='puede_crear_evento',
        name='Puede crear evento',
        content_type=content_type
    )
    Permission.objects.get_or_create(
        codename='puede_editar_evento',
        name='Puede editar evento',
        content_type=content_type
    )

    # Obtener los permisos una vez creados
    puede_crear = Permission.objects.get(codename='puede_crear_evento')
    puede_editar = Permission.objects.get(codename='puede_editar_evento')
    puede_eliminar = Permission.objects.get(codename='delete_evento')

    # Permisos base del modelo Evento
    permisos_base = Permission.objects.filter(content_type=content_type)

    # Asignar permisos por rol
    admin_group.permissions.set(permisos_base)
    organizador_group.permissions.set([puede_crear, puede_editar])
    asistente_group.permissions.clear()

