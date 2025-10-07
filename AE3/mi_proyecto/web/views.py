from django.shortcuts import render

def inicio(request):
    contexto = {'mensaje': '¡Hola desde Django!'}
    return render(request, 'web/inicio.html', contexto)

def pagina_estatica(request):
    return render(request, 'web/inicio.html')

# Create your views here.