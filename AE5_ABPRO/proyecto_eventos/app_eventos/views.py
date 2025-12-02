from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Evento
from django.urls import reverse_lazy

class ListaEventos(ListView):
    model = Evento
    template_name = "app_eventos/lista_eventos.html"
    context_object_name = "eventos"

    

class MisEventos(LoginRequiredMixin, ListView):
    model = Evento
    template_name = "app_eventos/mis_eventos.html"
    context_object_name = "eventos"

    def get_queryset(self):
        return Evento.objects.filter(autor=self.request.user)
    