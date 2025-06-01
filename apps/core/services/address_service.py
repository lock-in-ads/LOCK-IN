from apps.core.repository.address_repository import AddressRepository


def register_address(data):
    return AddressRepository.create(data)


def update_address(pk, data):
    return AddressRepository.update(pk, data)
