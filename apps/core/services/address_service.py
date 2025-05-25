from django.core.exceptions import ValidationError
from apps.core.repository.address_repository import AddressRepository


def register_address(data):
    return AddressRepository.create(data)
