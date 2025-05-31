from apps.administrativo.models import Locker


class LockerRepository:
    @staticmethod
    def create(data):
        return Locker.objects.create(**data)

    @staticmethod
    def list_lockers():
        return Locker.objects.filter(is_deleted=False).all()

    @staticmethod
    def get_by_number(number):
        return Locker.objects.filter(number=number).first()

    @staticmethod
    def detail(pk):
        return Locker.objects.get(id=pk)

    @staticmethod
    def update(data):
        return Locker.objects.update(**data)

    @staticmethod
    def soft_delete(data):
        data.is_deleted = True
        Locker.save()
        return data
