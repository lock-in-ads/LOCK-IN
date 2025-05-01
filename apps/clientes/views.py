from django.shortcuts import get_object_or_404, render, redirect
from apps.clientes.models import Client
from apps.clientes.forms import *

def clients(request):
    clients = Client.objects.all()
    return render(request, 'client/clients.html', {'clients': clients})

def add_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
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
            return redirect('clients')  
    else:
        form = ClientForm()
    return render(request, 'client/add_client.html', {'form': form})
