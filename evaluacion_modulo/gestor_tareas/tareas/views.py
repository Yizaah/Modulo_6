from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Tarea
from .forms import TareaForm


# ---------------------------
# REGISTRO
# ---------------------------
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("lista_tareas")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


# ---------------------------
# LISTA DE TAREAS
# ---------------------------
@login_required
def lista_tareas(request):
    tareas = Tarea.objects.filter(usuario=request.user)
    return render(request, "tareas/lista_tareas.html", {"tareas": tareas})


# ---------------------------
# DETALLE DE TAREA
# ---------------------------
@login_required
def detalle_tarea(request, id):
    tarea = get_object_or_404(Tarea, pk=id, usuario=request.user)
    return render(request, "tareas/detalle_tarea.html", {"tarea": tarea})


# ---------------------------
# AGREGAR TAREA
# ---------------------------
@login_required
def agregar_tarea(request):
    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuario = request.user
            tarea.save()
            return redirect("lista_tareas")
    else:
        form = TareaForm()

    return render(request, "tareas/agregar_tarea.html", {"form": form})


# ---------------------------
# ELIMINAR TAREA
# ---------------------------
@login_required
def eliminar_tarea(request, id):
    tarea = get_object_or_404(Tarea, pk=id, usuario=request.user)
    tarea.delete()
    return redirect("lista_tareas")
