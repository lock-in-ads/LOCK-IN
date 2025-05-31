from django.db import models
from apps.core.models import BaseModel, Address
from apps.clientes.models import Client
from apps.arduino.models import Card


class Enterprise(BaseModel):
    legal_name = models.CharField(max_length=255, verbose_name="Razão Social")
    business_name = models.CharField(
        max_length=255,
        verbose_name="Nome Fantasia"
    )
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ")
    email = models.CharField(max_length=255, verbose_name="Email")
    phone = models.CharField(max_length=14, verbose_name="Numero de telefone")
    description = models.TextField(verbose_name="Descrição")
    address = models.ManyToManyField(
        Address,
        related_name="entrepises",
        verbose_name="Endereços"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return str(self.legal_name)


class Locker(BaseModel):
    enterprise_id = models.ForeignKey(
        Enterprise,
        on_delete=models.PROTECT,
        related_name="lockers",
        verbose_name="ID da empresa"
    )
    card_id = models.ForeignKey(
        Card,
        on_delete=models.PROTECT,
        related_name="lockers",
        verbose_name="Cartão",
        null=True,
        blank=True
    )
    client_id = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="lockers",
        verbose_name="Cliente",
        null=True,
        blank=True
    )
    number = models.PositiveSmallIntegerField(verbose_name="Número do Armário")
    available = models.BooleanField(default=True, verbose_name="Disponivel")

    class Meta:
        ordering = ['-created_at', 'available', 'number']
        verbose_name = "Armário"
        verbose_name_plural = "Armários"

    def __str__(self):
        return str(self.number)
