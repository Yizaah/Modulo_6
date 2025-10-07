from django.shortcuts import render

# Create your views here.
def inicio(request):
    contexto = {'mensaje': 'Mensaje de prueba'}
    return render(request, 'mi_aplicacion/inicio.html', contexto)

def index(request):
    variable = "99"
    return render(request, 'mi_aplicacion/index.html', {"variable": variable})
