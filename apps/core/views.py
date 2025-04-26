from django.shortcuts import get_object_or_404, render, redirect
from apps.administrativo.models import Locker, Card
from apps.clientes.models import Client
from apps.core.forms import *

def quick_assignment(request):
    lockers = Locker.objects.order_by('number')
    return render(request, 'locker/quick_assignment.html', {"lockers": lockers})

def assign_locker(request, id):
    locker = get_object_or_404(Locker, id=id) 
    if request.method == "POST":
        form = LockerAssignmentForm(request.POST)
        if form.is_valid():            
            locker.available = form.cleaned_data['available']
            locker.client_id = form.cleaned_data['client']
            locker.save()
            return redirect('quick_assignment')  
    else:
        initial_locker_data = {
            'available': locker.available,
            'number': locker.number,
            'card': locker.card_id,
            'client': locker.client_id
        }
        form = LockerAssignmentForm(initial=initial_locker_data)   
    
    return render(request, 'locker/assign_locker.html', {'form': form})

def lockers(request):
    Lockers = Locker.objects.order_by('number')
    return render(request, 'locker/lockers.html', {"lockers": Lockers})

def add_locker(request):
    if request.method == "POST":
        form = LockerAddForm(request.POST)
        if form.is_valid(): 
            Locker.objects.create(
                available = form.cleaned_data['available'],
                number = form.cleaned_data['number'],
                card_id = form.cleaned_data['card'],
                enterprise_id = form.cleaned_data['enterprise']
            )
            return redirect('lockers')  
    else:
        form = LockerAddForm()
    
    return render(request, 'locker/add_locker.html', {'form': form})

def delete_locker():
    return render

def cards(request):
    cards = Card.objects.all()
    return render(request, 'card/cards.html', {'cards': cards})

def add_card(request):
    return render(request, 'card/add_card.html')

def users(request):
    users = Client.objects.all()
    return render(request, 'user/users.html', {'users': users})

def add_user(request):
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid(): 
            client_address = Address.objects.create(
                cep = form.cleaned_data['cep'],
                street = form.cleaned_data['street'],
                number = form.cleaned_data['number'],
                city = form.cleaned_data['city'],
                uf = form.cleaned_data['uf'],
                address_2 = form.cleaned_data['address_2'],
                reference_point = form.cleaned_data['reference_point']
            )
            
            client = Client.objects.create(
                name = form.cleaned_data['name'],
                phone = form.cleaned_data['phone'],
                email = form.cleaned_data['email'],
                access_level = form.cleaned_data['access_level']
            )

            client.address.add(client_address)

            return redirect('users')  
    else:
        form = UserAddForm()

    return render(request, 'user/add_user.html', {'form': form})