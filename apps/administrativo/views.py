from django.shortcuts import get_object_or_404, render, redirect
from apps.administrativo.models import Locker, Card
from django.core.exceptions import ValidationError
from apps.administrativo.forms import (
    LockerAssignmentForm,
    LockerForm,
    CardForm
)
from django.urls import reverse_lazy
from apps.administrativo.service.locker_service import (
    register_locker,
    list_relevant,
    detail,
    update_locker_data,
    delete
)
from django.contrib import messages
from django.db.models import ProtectedError
from django.views.generic import ListView
from django.views.generic.edit import (
    UpdateView,
    CreateView,
    DeleteView
)


class QuickAssignmentView(ListView):
    model = Locker
    template_name = 'locker/quick_assignment.html'
    context_object_name = 'lockers'

    def get_queryset(self):
        return list_relevant()


class AssignLockerView(UpdateView):
    model = Locker
    form_class = LockerAssignmentForm
    template_name = 'locker/assign_locker.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'locker'

    def get_initial(self):
        pk = self.kwargs.get('pk')
        if not pk:
            messages.error(self.request, "Esse item não existe.")

        try:
            locker = detail(pk)
            return {
                'available': locker.available,
                'number': locker.number,
                'card': locker.card_id,
                'client': locker.client_id
            }
        except ValidationError as e:
            messages.error(self, e.message)

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        if not pk:
            messages.error(self.request, "Esse item não existe.")

        locker = {
            'available': form.cleaned_data['available'],
            'client': form.cleaned_data['client']
        }

        update_locker_data(data=locker)
        return redirect('quick_assignment')


class ListLockersView(ListView):
    model = Locker
    template_name = 'locker/lockers.html'
    context_object_name = 'lockers'

    def get_queryset(self):
        return list_relevant()


class AddLockerView(CreateView):
    template_name = 'locker/add_locker.html'
    form_class = LockerForm
    success_url = reverse_lazy('lockers')

    def form_valid(self, form):
        """Handles valid form submission using the service layer."""
        locker_data = {
            'available': form.cleaned_data['available'],
            'number': form.cleaned_data['number'],
            'card_id': form.cleaned_data['card'],
            'enterprise_id': form.cleaned_data['enterprise']
        }

        try:
            register_locker(locker_data)
            messages.success(self.request, "Locker added successfully!")
            return super().form_valid(form)
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class UpdateLockerView(UpdateView):
    model = Locker
    form_class = LockerForm
    template_name = 'locker/update_locker.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'locker'

    def get_initial(self):
        pk = self.kwargs.get('pk')
        if not pk:
            messages.error(self.request, "Esse item não existe.")

        try:
            locker = detail(pk)
            return {
                'available': locker.available,
                'number': locker.number,
                'card': locker.card_id,
                'enterprise': locker.enterprise_id
            }
        except ValidationError as e:
            messages.error(self.request, str(e))
            return super().get_initial()

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        if not pk:
            messages.error(self.request, "Esse item não existe.")
            return redirect('lockers')

        locker_data = {
            'available': form.cleaned_data['available'],
            'number': form.cleaned_data['number'],
            'card': form.cleaned_data['card'],
            'enterprise': form.cleaned_data['enterprise']
        }

        try:
            update_locker_data(data=locker_data)
            messages.success(
                self.request,
                f"Armário {locker_data['number']} foi atualizado com sucesso!"
            )
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

        return redirect('lockers')


class DeleteLockerView(DeleteView):
    model = Locker
    pk_url_kwarg = 'pk'
    context_object_name = 'locker'
    success_url = reverse_lazy('lockers')
    template_name = 'locker/delete_locker.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        if not pk:
            messages.error(self.request, "Esse item não existe.")

        try:
            locker = detail(pk)
            return locker
        except ValidationError as e:
            messages.error(self.request, str(e))
        except Exception as e:
            messages.error(self.request, f"Erro ao carregar armário: {str(e)}")

    def delete(self, request, *args, **kwargs):
        locker = self.get_object()
        number = locker.number

        try:
            delete(data=locker)
            messages.success(
                request,
                f"Armário {number} foi excluído com sucesso!"
            )
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f"Erro ao excluir armário: {str(e)}")
            return redirect('lockers')


# TODO CHANGE THIS TO ARDUINO APP
# def cards(request):
#     cards = Card.objects.all()
#     return render(request, 'card/cards.html', {'cards': cards})


# def add_card(request):
#     return render(request, 'card/add_card.html')


# def update_card(request, pk):
#     card = get_object_or_404(Card, id=pk)
#     if request.method == "POST":
#         form = CardForm(request.POST)
#         if form.is_valid():
#             card.available = form.cleaned_data['available']
#             card.rfid = form.cleaned_data['rfid']
#             card.save()
#             messages.success(
#                 request,
#                 f"Cartão {card.id} - "
#                 f"RFID: {card.rfid} foi atualizado com sucesso!"
#             )
#             return redirect('cards')
#     else:
#         initial_card_data = {
#             'available': card.available,
#             'rfid': card.rfid,
#         }
#         form = CardForm(initial=initial_card_data)
#     return render(request, 'card/update_card.html', {'form': form})


# def delete_card(request, pk):
#     card = get_object_or_404(Card, id=pk)
#     if request.method == "POST":
#         card_details = f"{card.id} - RFID:{card.rfid}"
#         try:
#             card.delete()
#             messages.success(
#                 request,
#                 f"Cartão {card_details} foi excluído com sucesso!"
#             )
#         except ProtectedError:
#             messages.error(
#                 request,
#                 "Este cartão está sendo utilizado em um "
#                 "armário e não pode ser deletado!"
#             )
#         return redirect('cards')
