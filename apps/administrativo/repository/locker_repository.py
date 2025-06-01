from apps.administrativo.models import Locker


class LockerRepository:
    @staticmethod
    def create(data):
        return Locker.objects.create(**data)

    @staticmethod
    def list_lockers():
        return Locker.objects.filter(is_deleted=False).all().order_by('number')

    @staticmethod
    def get_by_number(number):
        return Locker.objects.filter(number=number).first()

    @staticmethod
    def detail(pk):
        return Locker.objects.get(id=pk)

    @staticmethod
    def update(pk, data):
        return Locker.objects.filter(id=pk).update(**data)

    @staticmethod
    def soft_delete(data):
        data.is_deleted = True
        data.save()
        return data
