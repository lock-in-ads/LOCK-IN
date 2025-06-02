from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from apps.clientes.models import Client
from apps.clientes.forms import ClientForm
from apps.clientes.service.client_service import (
    register_client,
    detail,
    get_address,
    add_address_to_client,
    delete,
    list_relevant,
    update_client,
)
from apps.core.services.address_service import (
    register_address,
    update_address
)
from django.contrib.auth.mixins import LoginRequiredMixin


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client/clients.html'
    context_object_name = 'clients'

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
            queryset = queryset.filter(name__icontains=name_search)

        if order_by:
            queryset = queryset.order_by(order_by)

        return queryset


class ClientCreateView(LoginRequiredMixin, View):
    template_name = 'client/add_client.html'

    def get(self, request):
        form = ClientForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ClientForm(request.POST)
        if form.is_valid():
            address_data = {
                'cep': form.cleaned_data['cep'],
                'street': form.cleaned_data['street'],
                'number': form.cleaned_data['number'],
                'city': form.cleaned_data['city'],
                'uf': form.cleaned_data['uf'],
                'address_2': form.cleaned_data['address_2'],
                'reference_point': form.cleaned_data['reference_point']
            }
            client_data = {
                'name': form.cleaned_data['name'],
                'phone': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'access_level': form.cleaned_data['access_level']
            }
            try:
                client = register_client(client_data)
                add_address_to_client(client, register_address(address_data))
                messages.success(request, "Usuário cadastrado com sucesso")
                return redirect('clients')
            except ValidationError as e:
                messages.error(request, e.message)

        return render(request, self.template_name, {'form': form})


class ClientUpdateView(LoginRequiredMixin, View):
    template_name = 'client/update_client.html'

    def get(self, request, pk):
        client = detail(pk)
        address = get_address(pk)
        initial_data = {
            'name': client.name,
            'phone': client.phone,
            'email': client.email,
            'access_level': client.access_level,
            'cep': address.cep,
            'street': address.street,
            'number': address.number,
            'city': address.city,
            'uf': address.uf,
            'address_2': address.address_2,
            'reference_point': address.reference_point
        }
        form = ClientForm(initial=initial_data)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        client = detail(pk)
        address = get_address(pk)
        form = ClientForm(request.POST)
        if form.is_valid():
            client_data = {
                'name':  form.cleaned_data['name'],
                'phone': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'access_level': form.cleaned_data['access_level']
            }

            address_data = {
                'cep': form.cleaned_data['cep'],
                'street': form.cleaned_data['street'],
                'number': form.cleaned_data['number'],
                'city': form.cleaned_data['city'],
                'uf': form.cleaned_data['uf'],
                'address_2': form.cleaned_data['address_2'],
                'reference_point': form.cleaned_data['reference_point']
            }

            update_client(pk=pk, data=client_data)
            update_address(pk=address.id, data=address_data)

            messages.success(
                request, f"Usuário {client.name} foi atualizado com sucesso!"
            )
            return redirect('clients')
        return render(request, self.template_name, {'form': form})


class ClientDeleteView(LoginRequiredMixin, View):
    template_name = 'client/confirm_delete.html'

    def get(self, request, pk):
        client = detail(pk=pk)
        return render(request, self.template_name, {'client': client})

    def post(self, request, pk):
        client = detail(pk)
        name = client.name
        delete(client)
        messages.success(request, f"Usuário {name} foi excluído com sucesso!")
        return redirect('clients')
