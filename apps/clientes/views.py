from django.views import View
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from apps.clientes.models import Client
from apps.clientes.forms import ClientForm
from apps.clientes.service.client_service import (
    register_client,
    add_address_to_client,
    delete,
    list_clients
)
from apps.core.services.address_service import register_address


class ClientListView(ListView):
    model = Client
    template_name = 'client/clients.html'
    context_object_name = 'clients'

    def get_queryset(self):
        return list_clients()


class ClientCreateView(View):
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


class ClientUpdateView(View):
    template_name = 'client/update_client.html'

    def get(self, request, pk):
        client = get_object_or_404(Client, id=pk)
        address = client.address.first()
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
        client = get_object_or_404(Client, id=pk)
        address = client.address.first()
        form = ClientForm(request.POST)
        if form.is_valid():
            client.name = form.cleaned_data['name']
            client.phone = form.cleaned_data['phone']
            client.email = form.cleaned_data['email']
            client.access_level = form.cleaned_data['access_level']

            address.cep = form.cleaned_data['cep']
            address.street = form.cleaned_data['street']
            address.number = form.cleaned_data['number']
            address.city = form.cleaned_data['city']
            address.uf = form.cleaned_data['uf']
            address.address_2 = form.cleaned_data['address_2']
            address.reference_point = form.cleaned_data['reference_point']

            client.save()
            address.save()

            messages.success(
                request, f"Usuário {client.name} foi atualizado com sucesso!"
            )
            return redirect('clients')
        return render(request, self.template_name, {'form': form})


class ClientDeleteView(View):
    template_name = 'client/confirm_delete.html'

    def get(self, request, pk):
        client = get_object_or_404(Client, id=pk)
        return render(request, self.template_name, {'client': client})

    def post(self, request, pk):
        client = get_object_or_404(Client, id=pk)
        name = client.name
        delete(client)
        messages.success(request, f"Usuário {name} foi excluído com sucesso!")
        return redirect('clients')
