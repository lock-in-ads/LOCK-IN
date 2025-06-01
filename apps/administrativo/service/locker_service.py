from apps.administrativo.repository.locker_repository import LockerRepository
from django.core.exceptions import ValidationError


def register_locker(data):
    if LockerRepository.get_by_number(data['number']):
        raise ValidationError('Esse armário já existe')
    return LockerRepository.create(data)


def list_relevant():
    return LockerRepository.list_lockers()


def detail(pk):
    locker = LockerRepository.detail(pk=pk)
    if locker.is_deleted:
        return ValidationError("Esse armário não pode ser acessado pois foi excluído")
    return locker


def update_locker_data(data):
    return LockerRepository.update(data)


def delete(data):
    return LockerRepository.soft_delete(data)
