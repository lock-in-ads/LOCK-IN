from django.shortcuts import get_object_or_404, render, redirect
from apps.administrativo.models import Locker, Card
from django.core.exceptions import ValidationError
from apps.administrativo.forms import (
    LockerAssignmentForm,
    LockerForm,
    CardForm
)
from apps.administrativo.service.locker_service import (
    register_locker,
    list_relevant,
    update_locker_data,
    delete
)
from django.contrib import messages
from django.db.models import ProtectedError
from django.views.generic import ListView
from django.views.generic.edit import UpdateView


class QuickAssignmentView(ListView):
    model = Locker
    template_name = 'locker/quick_assignment.html'
    context_object_name = 'lockers'
    ordering = ['number']


class AssignLockerView(UpdateView):
    model = Locker
    form_class = LockerAssignmentForm
    template_name = 'locker/assign_locker.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'locker'

    def get_initial(self):
        locker = self.get_object()
        return {
            'available': locker.available,
            'number': locker.number,
            'card': locker.card_id,
            'client': locker.client_id
        }

    def form_valid(self, form):
        locker = self.get_object()
        locker.available = form.cleaned_data['available']
        locker.client_id = form.cleaned_data['client']
        locker.save()
        return redirect('quick_assignment')


def lockers(request):
    Lockers = list_relevant()
    return render(request, 'locker/lockers.html', {"lockers": Lockers})


def add_locker(request):
    if request.method == "POST":
        form = LockerForm(request.POST)
        if form.is_valid():
            locker = {
                'available': form.cleaned_data['available'],
                'number': form.cleaned_data['number'],
                'card_id': form.cleaned_data['card'],
                'enterprise_id': form.cleaned_data['enterprise']
            }
            try:
                register_locker(locker)
            except ValidationError as e:
                messages.error(request, e.message)
            return redirect('lockers')
    else:
        form = LockerForm()
    return render(request, 'locker/add_locker.html', {'form': form})


def update_locker(request, pk):
    locker = get_object_or_404(Locker, id=pk)
    if request.method == "POST":
        form = LockerForm(request.POST)
        if form.is_valid():
            locker_data = {
                'available': form.cleaned_data['available'],
                'number': form.cleaned_data['number'],
                'card': form.cleaned_data['card'],
                'enterprise': form.cleaned_data['enterprise']
            }
            update_locker_data(data=locker_data)
            locker.save()
            messages.success(
                request,
                f"Armário {locker.number} foi atualizado com sucesso!"
            )
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
        delete(data=locker)
        messages.success(
            request,
            f"Armário {number} foi excluído com sucesso!"
        )
        return redirect('lockers')


def cards(request):
    cards = Card.objects.all()
    return render(request, 'card/cards.html', {'cards': cards})


def add_card(request):
    return render(request, 'card/add_card.html')


def update_card(request, pk):
    card = get_object_or_404(Card, id=pk)
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            card.available = form.cleaned_data['available']
            card.rfid = form.cleaned_data['rfid']
            card.save()
            messages.success(
                request,
                f"Cartão {card.id} - "
                f"RFID: {card.rfid} foi atualizado com sucesso!"
            )
            return redirect('cards')
    else:
        initial_card_data = {
            'available': card.available,
            'rfid': card.rfid,
        }
        form = CardForm(initial=initial_card_data)
    return render(request, 'card/update_card.html', {'form': form})


def delete_card(request, pk):
    card = get_object_or_404(Card, id=pk)
    if request.method == "POST":
        card_details = f"{card.id} - RFID:{card.rfid}"
        try:
            card.delete()
            messages.success(
                request,
                f"Cartão {card_details} foi excluído com sucesso!"
            )
        except ProtectedError:
            messages.error(
                request,
                "Este cartão está sendo utilizado em um "
                "armário e não pode ser deletado!"
            )
        return redirect('cards')
