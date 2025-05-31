from apps.administrativo.repository.locker_repository import LockerRepository
from django.core.exceptions import ValidationError


def register_locker(data):
    if LockerRepository.get_by_number(data['number']):
        raise ValidationError('Esse armário já existe')
    return LockerRepository.create(data)


def list_relevant():
    return LockerRepository.list_lockers()


def detail(pk):
    return LockerRepository.detail(pk=pk)


def update_locker_data(data):
    return LockerRepository.update(data)


def delete(data):
    return LockerRepository.soft_delete(data)
