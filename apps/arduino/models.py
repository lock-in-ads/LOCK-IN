from django.db import models
from apps.core.models import BaseModel
from apps.administrativo.models import Enterprise


class Card(BaseModel):
    enterprise_id = models.ForeignKey(
        Enterprise,
        on_delete=models.PROTECT,
        related_name="cards",
        verbose_name="ID da empresa"
    )
    rfid = models.CharField(max_length=8, verbose_name="RFID")
    available = models.BooleanField(default=True, verbose_name="Disponivel")

    class Meta:
        ordering = ['-created_at', 'available']
        verbose_name = "Cartão"
        verbose_name_plural = "Cartões"

    def __str__(self):
        return str(self.id)
