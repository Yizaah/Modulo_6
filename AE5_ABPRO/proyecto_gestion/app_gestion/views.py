from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Evento
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


# Página principal
def home(request):
    return render(request, 'home.html')


# Registro de usuario
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado correctamente. Ya puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, '❌ Ocurrió un error al registrar el usuario. Revisa los datos.')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

#login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()   # <-- ESTA es la diferencia
            login(request, user)
            return redirect("lista_eventos")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})



#  Listado de eventos (solo usuarios autenticados)
class ListaEventosView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'lista_eventos.html'
    context_object_name = 'eventos'
    login_url = 'login'


#  Crear evento (requiere permiso personalizado)
class CrearEventoView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Evento
    fields = ['nombre', 'descripcion', 'fecha']
    template_name = 'crear_evento.html'
    success_url = reverse_lazy('lista_eventos')
    permission_required = 'app_gestion.puede_crear_evento'
    raise_exception = True

    def form_valid(self, form):
        evento = form.save(commit=False)   # No lo guardes aún
        evento.organizador = self.request.user  # Asignar usuario logueado
        evento.save()  # Ahora sí guardar
        messages.success(self.request, "Evento creado correctamente.")
        return redirect(self.success_url)

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para crear eventos.")
        return redirect('acceso_denegado')



# Editar evento (requiere permiso)
class EditarEventoView(PermissionRequiredMixin, UpdateView):
    model = Evento
    fields = ['nombre', 'descripcion', 'fecha']
    template_name = 'editar_evento.html'  # o 'evento_form.html' si es compartida
    success_url = reverse_lazy('lista_eventos')
    permission_required = 'app_gestion.puede_editar_evento'
    raise_exception = False

    def form_valid(self, form):
        messages.success(self.request, 'Evento actualizado correctamente.')
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para editar este evento.")
        return redirect('acceso_denegado')


# Eliminar evento (solo administradores)
class EliminarEventoView(PermissionRequiredMixin, DeleteView):
    model = Evento
    template_name = 'eliminar_evento.html'
    success_url = reverse_lazy('lista_eventos')
    permission_required = 'app_gestion.delete_evento'
    raise_exception = False

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Evento eliminado correctamente.')
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para eliminar eventos.")
        return redirect('acceso_denegado')


def acceso_denegado(request):
    messages.error(request, "No tienes permiso para acceder a esta sección.")
    return render(request, 'acceso_denegado.html')