from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Evento
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings


def home(request):
    return HttpResponse("Plataforma de Gestión de Eventos")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'eventos/login.html')


def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

def acceso_denegado(request):
    messages.error(request, 'No tienes permisos para acceder a esta sección.')
    return render(request, 'eventos/acceso_denegado.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Usuario creado correctamente')
            return redirect('/login/')

    return render(request, 'eventos/register.html')

class EventoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Evento
    fields = ['titulo', 'descripcion', 'tipo', 'fecha', 'es_privado']
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('home')

    permission_required = 'eventos.add_evento'

    def form_valid(self, form):
        form.instance.organizador = self.request.user
        return super().form_valid(form)

class EventoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Evento
    fields = ['titulo', 'descripcion', 'tipo', 'fecha', 'es_privado']
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('home')

    permission_required = 'eventos.change_evento'
    raise_exception = False

    def handle_no_permission(self):
        messages.error(
            self.request,
            'No tienes permisos para editar este evento.'
        )
        return redirect('acceso_denegado')

class EventoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Evento
    template_name = 'eventos/evento_confirm_delete.html'
    success_url = reverse_lazy('home')

    permission_required = 'eventos.delete_evento'
    raise_exception = False

    def handle_no_permission(self):
        messages.error(
            self.request,
            'No tienes permisos para eliminar este evento.'
        )
        return redirect('acceso_denegado')
        return redirect('acceso_denegado')

class EventoDetailView(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = 'eventos/evento_detail.html'

    def dispatch(self, request, *args, **kwargs):
        evento = self.get_object()

        if evento.es_privado:
            if (
                request.user != evento.organizador and
                request.user not in evento.asistentes.all() and
                not request.user.has_perm('eventos.view_evento')
            ):
                messages.error(
                    request,
                    'Este evento es privado y no tienes acceso.'
                )
                return redirect('acceso_denegado')

        return super().dispatch(request, *args, **kwargs)
