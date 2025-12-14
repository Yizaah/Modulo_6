# Plataforma de Gestión de Eventos

Aplicación sencilla en Django para crear, gestionar y asistir a eventos. Las plantillas y la interfaz están en español.

## Funcionalidades
- Registro e inicio de sesión de usuarios (Django auth)
- Crear, editar, eliminar, listar y ver eventos
- Eventos privados: sólo el organizador, los asistentes o usuarios con el permiso `view_evento` pueden acceder
- Tipos de evento: `conferencia`, `concierto`, `seminario`
- Interfaz de administración para gestionar eventos

## Requisitos
- Python 3.8+ (compatible con Django 6.0)
- pip

Nota: El proyecto usa SQLite por defecto (`db.sqlite3`) para desarrollo.

## Inicio rápido (Desarrollo)
1. Crear y activar un entorno virtual

   Windows (PowerShell):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   CMD:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

2. Instalar Django (6.0) o las dependencias necesarias

```bash
pip install Django==6.0
# o usar un requirements.txt si lo agregas
``` 

3. Aplicar migraciones y crear un superusuario

```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

5. Visitar:
- Aplicación: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Autenticación y URLs
- Login: `/login/` (LoginView de Django)
- Logout: `/logout/` (LogoutView de Django)
- Registro: `/register/` (vista personalizada en `eventos.views.register`)
- Lista de eventos: `/eventos/`
- Crear evento: `/eventos/crear/` (requiere permiso `add_evento`)
- Detalle de evento: `/eventos/<pk>/`
- Editar: `/eventos/<pk>/editar/` (requiere `change_evento`)
- Eliminar: `/eventos/<pk>/eliminar/` (requiere `delete_evento`)

## Modelos
- `Evento` (en `eventos.models`)
  - `titulo` - CharField
  - `descripcion` - TextField
  - `tipo` - CharField (opciones: conferencia, concierto, seminario)
  - `fecha` - DateTimeField
  - `es_privado` - BooleanField
  - `organizador` - ForeignKey a `User`
  - `asistentes` - ManyToManyField a `User`

Privacidad: Los eventos privados (`es_privado=True`) solo se muestran al organizador, a los asistentes, o a usuarios con el permiso `view_evento`. Los superusuarios pueden ver todos los eventos.

## Administración
El modelo `Evento` está registrado en `eventos/admin.py` y ofrece una interfaz administrativa básica para gestionar eventos.

## Ejecutar pruebas
Ejecuta la suite de pruebas de Django:

```bash
python manage.py test
```

## Notas y próximos pasos
- La configuración está orientada a desarrollo (`DEBUG=True`) y usa una clave secreta fija — no usar en producción.
- Las plantillas están en español; si lo deseas, puedes traducirlas o ajustar `LANGUAGE_CODE` en `settings.py`.

## Estructura del proyecto
- `plataforma_eventos/` - Ajustes del proyecto y rutas
- `eventos/` - App con modelos, vistas y plantillas
- `db.sqlite3` - Base de datos SQLite para desarrollo
