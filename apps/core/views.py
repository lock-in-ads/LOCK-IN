from django.shortcuts import render

# Create your views here.
def cadastrarusuario(request):
    return render(request, 'cadastrar-usuario.html')
