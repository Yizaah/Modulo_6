from django.shortcuts import render

# Create your views here.
def inicio(request):
    contexto = {'mensaje': '¡Los que vamos a morir te saludan!'}
    return render(request, 'mi_aplicacion/inicio.html', contexto)
