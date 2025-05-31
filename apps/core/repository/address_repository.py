from apps.core.models import Address


class AddressRepository:
    @staticmethod
    def create(data):
        return Address.objects.create(**data)

    @staticmethod
    def update(data):
        return Address.objects.update(**data)

    @staticmethod
    def get_by_street(street):
        return Address.objects.filter(street=street).all()
