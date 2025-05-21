from django.shortcuts import get_object_or_404, render, redirect
from apps.clientes.models import Client, Address
from apps.clientes.forms import ClientForm
from django.contrib import messages


def clients(request):
    clients = Client.objects.all()
    return render(request, 'client/clients.html', {'clients': clients})


def add_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client_address = Address.objects.create(
                cep=form.cleaned_data['cep'],
                street=form.cleaned_data['street'],
                number=form.cleaned_data['number'],
                city=form.cleaned_data['city'],
                uf=form.cleaned_data['uf'],
                address_2=form.cleaned_data['address_2'],
                reference_point=form.cleaned_data['reference_point']
            )
            client = Client.objects.create(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                access_level=form.cleaned_data['access_level']
            )
            client.address.add(client_address)
            return redirect('clients')
    else:
        form = ClientForm()
    return render(request, 'client/add_client.html', {'form': form})


def update_client(request, pk):
    client = get_object_or_404(Client, id=pk)
    address = client.address.first()
    if request.method == "POST":
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
            address.save()

            client.save()
            messages.success(
                request,
                f"Usuário {client.name} foi atualizado com sucesso!"
            )
            return redirect('clients')
    else:
        initial_client_data = {
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
        form = ClientForm(initial=initial_client_data)
    return render(request, 'client/update_client.html', {'form': form})


def delete_client(request, pk):
    client = get_object_or_404(Client, id=pk)
    if request.method == "POST":
        name = client.name
        client.delete()
        messages.success(request, f"Usuário {name} foi excluído com sucesso!")
        return redirect('clients')
