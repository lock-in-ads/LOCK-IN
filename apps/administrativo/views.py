from django.shortcuts import get_object_or_404, render, redirect
from apps.administrativo.models import Locker, Card
from apps.administrativo.forms import *
from django.contrib import messages

def quick_assignment(request):
    lockers = Locker.objects.order_by('number')
    return render(request, 'locker/quick_assignment.html', {"lockers": lockers})

def assign_locker(request, pk):
    locker = get_object_or_404(Locker, id=pk) 
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
    return render(request, 'locker/assign_locker.html', {'form': form, 'locker': locker})

def lockers(request):
    Lockers = Locker.objects.order_by('number')
    return render(request, 'locker/lockers.html', {"lockers": Lockers})

def add_locker(request):
    if request.method == "POST":
        form = LockerForm(request.POST)
        if form.is_valid(): 
            Locker.objects.create(
                available = form.cleaned_data['available'],
                number = form.cleaned_data['number'],
                card_id = form.cleaned_data['card'],
                enterprise_id = form.cleaned_data['enterprise']
            )
            return redirect('lockers')  
    else:
        form = LockerForm()
    return render(request, 'locker/add_locker.html', {'form': form})

def update_locker(request, pk):
    locker = get_object_or_404(Locker, id=pk) 
    if request.method == "POST":
        form = LockerForm(request.POST)
        if form.is_valid():            
            locker.available = form.cleaned_data['available']
            locker.number = form.cleaned_data['number']
            locker.card_id = form.cleaned_data['card']
            locker.enterprise_id = form.cleaned_data['enterprise']
            locker.save()
            messages.success(request, f"Armário {locker.number} foi atualizado com sucesso!")
            return redirect('lockers')  
    else:
        initial_locker_data = {
            'available': locker.available,
            'number': locker.number,
            'card': locker.card_id,
            'enterprise': locker.enterprise_id
        }
        form = LockerForm(initial=initial_locker_data)
    return render(request, 'locker/update_locker.html', {'form': form})

def delete_locker(request, pk):
    locker = get_object_or_404(Locker, id=pk)
    if request.method == "POST":
        number = locker.number
        locker.delete()
        messages.success(request, f"Armário {number} foi excluído com sucesso!")
        return redirect('lockers')

def cards(request):
    cards = Card.objects.all()
    return render(request, 'card/cards.html', {'cards': cards})

def add_card(request):
    return render(request, 'card/add_card.html')