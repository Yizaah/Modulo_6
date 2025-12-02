from django.shortcuts import render, redirect
from django.http import Http404
from .forms import TareaForm

# Lista en memoria para almacenar las tareas
TAREAS = [
    {"id": 1, "titulo": "Tarea de ejemplo", "descripcion": "Esta es una tarea inicial"}
]

def lista_tareas(request):
    context = {
        "tareas": TAREAS
    }
    return render(request, "tareas/lista_tareas.html", context)

def detalle_tarea(request, id):
    # Buscar la tarea por ID
    tarea = next((t for t in TAREAS if t["id"] == id), None)

    if tarea is None:
        raise Http404("La tarea no existe")

    context = {"tarea": tarea}
    return render(request, "tareas/detalle_tarea.html", context)

def agregar_tarea(request):
    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            nuevo_id = TAREAS[-1]["id"] + 1 if TAREAS else 1
            
            nueva_tarea = {
                "id": nuevo_id,
                "titulo": form.cleaned_data["titulo"],
                "descripcion": form.cleaned_data["descripcion"],
            }
            TAREAS.append(nueva_tarea)

            return redirect("lista_tareas")
    else:
        form = TareaForm()

    return render(request, "tareas/agregar_tarea.html", {"form": form})

def eliminar_tarea(request, id):
    global TAREAS

    # Buscar la tarea
    tarea = next((t for t in TAREAS if t["id"] == id), None)

    if tarea is None:
        raise Http404("La tarea no existe")

    if request.method == "POST":
        # Eliminar la tarea
        TAREAS = [t for t in TAREAS if t["id"] != id]
        return redirect("lista_tareas")

    # Página de confirmación
    return render(request, "tareas/eliminar_tarea.html", {"tarea": tarea})
