from django.db import models
from apps.core.models import BaseModel


class Card(BaseModel):
    rfid = models.CharField(max_length=8, verbose_name="RFID")
    available = models.BooleanField(default=True, verbose_name="Disponivel")

    class Meta:
        ordering = ['-created_at', 'available']
        verbose_name = "Cartão"
        verbose_name_plural = "Cartões"

    def __str__(self):
        return str(self.rfid)
