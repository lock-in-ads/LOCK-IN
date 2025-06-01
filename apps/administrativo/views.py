from django.views import View
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
    perform_delete
)
from django.contrib import messages
from django.db.models import ProtectedError
from django.views.generic import ListView
from django.views.generic.edit import (
    UpdateView,
    CreateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

class QuickAssignmentView(LoginRequiredMixin, ListView):
    model = Locker
    template_name = 'locker/quick_assignment.html'
    context_object_name = 'lockers'

    def get_queryset(self):
        return list_relevant()


class AssignLockerView(LoginRequiredMixin, UpdateView):
    model = Locker
    form_class = LockerAssignmentForm
    template_name = 'locker/assign_locker.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'locker'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        return kwargs

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

        locker_data = {
            'available': form.cleaned_data['available'],
            'client': form.cleaned_data['client']
        }

        update_locker_data(pk=pk, data=locker_data)
        return redirect('quick_assignment')


class ListLockersView(LoginRequiredMixin, ListView):
    model = Locker
    template_name = 'locker/lockers.html'
    context_object_name = 'lockers'

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', 5)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_copy = self.request.GET.copy()
        if get_copy.get('page'):
            get_copy.pop('page')
        context['get_copy'] = get_copy
        return context
    
    def get_queryset(self):
        queryset = list_relevant()
        name_search = self.request.GET.get('name_search')
        order_by = self.request.GET.get('order_by')

        if name_search:
            queryset = queryset.filter(Q(client__name__icontains=name_search))
        
        if order_by:
            queryset = queryset.order_by(order_by)        
        
        return queryset


class AddLockerView(LoginRequiredMixin, CreateView):
    model = Locker
    form_class = LockerForm
    template_name = 'locker/add_locker.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        return kwargs

    def form_valid(self, form):
        locker_data = {
            'available': form.cleaned_data['available'],
            'number': form.cleaned_data['number'],
            'card': form.cleaned_data['card'],
            'enterprise': form.cleaned_data['enterprise']
        }

        try:
            register_locker(locker_data)
            messages.success(self.request, "Armário adicionado com sucesso!")
            return redirect('lockers')
        except ValidationError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)


class UpdateLockerView(LoginRequiredMixin, UpdateView):
    template_name = 'locker/update_locker.html'

    def get_queryset(self):
        return list_relevant()

    def get(self, request, pk):
        if not pk:
            messages.error(self.request, "Esse item não existe.")

        try:
            locker = detail(pk=pk)
            initial_data = {
                'available': locker.available,
                'number': locker.number,
                'card': locker.card,
                'enterprise': locker.enterprise
            }
            form = LockerForm(initial=initial_data)
            return render(request, self.template_name, {'form': form})
        except ValidationError as e:
            messages.error(self.request, str(e))
            return None
        except Exception as e:
            messages.error(self.request, f"Erro ao carregar armário: {str(e)}")
            return None

    def post(self, request, pk):
        if not pk:
            messages.error(self.request, "Esse item não existe.")

        locker = detail(pk=pk)
        if not locker:
            return redirect('lockers')

        form = LockerForm(request.POST)
        if form.is_valid():
            locker_data = {
                'available': form.cleaned_data['available'],
                'number': form.cleaned_data['number'],
                'card': form.cleaned_data['card'],
                'enterprise': form.cleaned_data['enterprise']
            }

        try:
            update_locker_data(pk=pk, data=locker_data)
            messages.success(
                self.request,
                f"Armário {locker_data['number']} foi atualizado com sucesso!"
            )
            return redirect('lockers')
        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

class DeleteLockerView(LoginRequiredMixin, DeleteView):
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
            perform_delete(data=locker)
            messages.success(
                request,
                f"Armário {number} foi excluído com sucesso!"
            )
            return redirect('lockers')
        except Exception as e:
            messages.error(request, f"Erro ao excluir armário: {str(e)}")
            return redirect('lockers')

    def form_valid(self, form):
        return self.delete(self.request)


# TODO CHANGE THIS TO ARDUINO APP
class CardListView(LoginRequiredMixin, View):
    def get(self, request):
        cards = Card.objects.all()
        return render(request, 'card/cards.html', {'cards': cards})

class CardAddView(LoginRequiredMixin, View):
    def get(self, request):
        form = CardForm()
        return render(request, 'card/add_card.html', {'form': form})

    def post(self, request):
        form = CardForm(request.POST)
        if form.is_valid():
            # Como não é ModelForm, crie manualmente o objeto
            card = Card(
                available=form.cleaned_data['available'],
                rfid=form.cleaned_data['rfid']
            )
            card.save()
            messages.success(request, f"Cartão {card.id} - RFID: {card.rfid} criado com sucesso!")
            return redirect('cards')
        return render(request, 'card/add_card.html', {'form': form})

class CardUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        card = get_object_or_404(Card, id=pk)
        initial_data = {
            'available': card.available,
            'rfid': card.rfid,
        }
        form = CardForm(initial=initial_data)
        return render(request, 'card/update_card.html', {'form': form, 'card': card})

    def post(self, request, pk):
        card = get_object_or_404(Card, id=pk)
        form = CardForm(request.POST)
        if form.is_valid():
            card.available = form.cleaned_data['available']
            card.rfid = form.cleaned_data['rfid']
            card.save()
            messages.success(request, f"Cartão {card.id} - RFID: {card.rfid} foi atualizado com sucesso!")
            return redirect('cards')
        return render(request, 'card/update_card.html', {'form': form, 'card': card})


class CardDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        card = get_object_or_404(Card, id=pk)
        card_details = f"{card.id} - RFID:{card.rfid}"
        try:
            card.delete()
            messages.success(request, f"Cartão {card_details} foi excluído com sucesso!")
        except ProtectedError:
            messages.error(request, "Este cartão está sendo utilizado em um armário e não pode ser deletado!")
        return redirect('cards')
