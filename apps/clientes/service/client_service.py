from apps.clientes.repository.client_repository import ClientRepository
from django.core.exceptions import ValidationError


def register_client(data):
    if ClientRepository.get_by_name(data['name']):
        raise ValidationError("Já existe esse usuário no sistema")
    return ClientRepository.create(data)


def add_address_to_client(client, address):
    return ClientRepository.link_address(client, address)


def detail(pk):
    return ClientRepository.detail(pk)


def get_address(pk):
    return ClientRepository.get_address(pk)


def delete(data):
    return ClientRepository.soft_delete(data)


def update_client(pk, data):
    print(data['name'])
    return ClientRepository.update(pk, data)


def get_by_name():
    return ClientRepository.get_by_name()


def list_relevant():
    return ClientRepository.list_active()
