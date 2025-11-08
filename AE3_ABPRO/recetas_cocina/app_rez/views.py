from django.shortcuts import render, get_object_or_404, redirect
import logging
from django.contrib import messages
from .models import Recipe, ContactMessage


def index(request):
    # Mostrar un mensaje de bienvenida y las últimas recetas
    latest_recipes = Recipe.objects.all()[:3]
    return render(request, 'index.html', {'latest_recipes': latest_recipes})


def recetas(request):
    recipes = Recipe.objects.all()
    return render(request, 'recetas.html', {'recipes': recipes})


def receta_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, 'recetas/receta_detail.html', {'recipe': recipe})


def contacto(request):
    # Validación server-side: mostrar warning si faltan campos
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        asunto = request.POST.get('asunto', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()

        if not (nombre and email and asunto and mensaje):
            messages.warning(request, "Por favor completa todos los campos antes de enviar.")
            # Re-renderizar con los valores proporcionados para que el usuario no pierda lo escrito
            return render(request, 'contacto.html', {
                'nombre': nombre,
                'email': email,
                'asunto': asunto,
                'mensaje': mensaje
            })

        # Guardar el mensaje en la base de datos con manejo de errores
        logger = logging.getLogger(__name__)
        try:
            ContactMessage.objects.create(
                name=nombre,
                email=email,
                subject=asunto,
                message=mensaje
            )
        except Exception as e:
            # Loguear la excepción y mostrar un mensaje amigable al usuario
            logger.exception("Error al guardar ContactMessage")
            messages.error(request, "Ocurrió un error al enviar tu mensaje. Por favor intenta de nuevo más tarde.")
            return render(request, 'contacto.html', {
                'nombre': nombre,
                'email': email,
                'asunto': asunto,
                'mensaje': mensaje
            })

        messages.success(request, f"Gracias {nombre}, tu mensaje ha sido enviado correctamente.")
        # Redirigir a la página de confirmación después de guardar el mensaje
        return redirect('contacto_ok')

    return render(request, 'contacto.html')


def custom_404(request, exception=None):
    """Vista que renderiza la plantilla 404 personalizada."""
    return render(request, '404.html', status=404)


def contacto_ok(request):
    """Página simple que confirma que el mensaje fue enviado correctamente."""
    return render(request, 'contacto_ok.html')


# Create your views here.
