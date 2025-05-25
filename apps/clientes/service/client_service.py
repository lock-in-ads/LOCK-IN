from apps.clientes.repository.client_repository import ClientRepository
from django.core.exceptions import ValidationError


def register_client(data):
    if ClientRepository.get_by_name(data['name']):
        raise ValidationError("Já existe esse usuário no sistema")
    return ClientRepository.create(data)


def add_address_to_client(client, address):
    return ClientRepository.link_address(client, address)


def delete(data):
    return ClientRepository.soft_delete(data)


def list_clients():
    return ClientRepository.list_active()
