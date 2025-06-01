from django.db import models
from apps.core.models import BaseModel, Address


class Client(BaseModel):
    class LevelChoices(models.IntegerChoices):
        SUPER_USER = 0, 'Super Usuário'
        MANAGER = 1, 'Gerente'
        SIMPLE_USER = 2, 'Cliente'

    name = models.CharField(max_length=255, verbose_name="Nome")
    phone = models.CharField(max_length=14, verbose_name="Número de telefone")
    email = models.CharField(max_length=255, verbose_name="Email")
    access_level = models.IntegerField(
        choices=LevelChoices.choices,
        default=LevelChoices.SIMPLE_USER,
        verbose_name="Nivel de acesso"
    )
    address = models.ManyToManyField(Address, related_name="usuarios")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return str(self.name)
