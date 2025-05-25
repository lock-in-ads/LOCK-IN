from apps.clientes.models import Client


class ClientRepository:
    @staticmethod
    def create(data):
        return Client.objects.create(**data)

    @staticmethod
    def get_by_name(name):
        return Client.objects.filter(name=name).first()

    @staticmethod
    def soft_delete(data):
        data.is_deleted = True
        Client.save(data)
        return data

    @staticmethod
    def link_address(client, address):
        return client.address.add(address)

    @staticmethod
    def list_all():
        return Client.objects.all()

    @staticmethod
    def list_active():
        return Client.objects.filter(is_deleted=False).all()
