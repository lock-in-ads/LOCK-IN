from django.shortcuts import render
from apps.administrativo.models import Locker
from apps.clientes.models import Client

def quick_assignment(request):
    lockers = Locker.objects.all()
    return render(request, 'quick-assignment.html', {"lokers": lockers})

def register_card(request):
    return render(request, 'register-card.html')

def list_users(request):
    users = Client.objects.all()
    return render(request, 'user-list.html', {"users": users})