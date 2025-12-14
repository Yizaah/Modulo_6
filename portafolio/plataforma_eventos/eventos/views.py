from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Evento
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.urls import reverse
from .forms import UserRegistrationForm
from django.conf import settings
from django.db.models import Q


def home(request):
    return render(request, 'eventos/home.html')

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


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create inactive user and send activation email
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(
                reverse('activate', args=[uid, token])
            )

            subject = 'Activa tu cuenta'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            send_mail(subject, message, None, [user.email])

            messages.success(request, 'Se ha enviado un correo de activación a tu email.')
            return redirect('register_done')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        messages.success(request, 'Cuenta activada correctamente.')
        return redirect('home')
    else:
        messages.error(request, 'El enlace de activación no es válido.')
        return redirect('register')


def register_done(request):
    return render(request, 'registration/activation_sent.html')

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

class EventoListView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'eventos/evento_list.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Evento.objects.all()

        return Evento.objects.filter(
            Q(es_privado=False) |
            Q(organizador=user) |
            Q(asistentes=user)
        ).distinct()

