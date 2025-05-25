from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(
        verbose_name="Está excluido?",
        default=False
    )

    class Meta:
        abstract = True


class Address(BaseModel):
    class UF_Choices(models.TextChoices):
        AC = 'AC', 'Acre'
        AL = 'AL', 'Alagoas'
        AP = 'AP', 'Amapá'
        AM = 'AM', 'Amazonas'
        BA = 'BA', 'Bahia'
        CE = 'CE', 'Ceará'
        DF = 'DF', 'Distrito Federal'
        ES = 'ES', 'Espírito Santo'
        GO = 'GO', 'Goiás'
        MA = 'MA', 'Maranhão'
        MT = 'MT', 'Mato Grosso'
        MS = 'MS', 'Mato Grosso do Sul'
        MG = 'MG', 'Minas Gerais'
        PA = 'PA', 'Pará'
        PB = 'PB', 'Paraíba'
        PR = 'PR', 'Paraná'
        PE = 'PE', 'Pernambuco'
        PI = 'PI', 'Piauí'
        RJ = 'RJ', 'Rio de Janeiro'
        RN = 'RN', 'Rio Grande do Norte'
        RS = 'RS', 'Rio Grande do Sul'
        RO = 'RO', 'Rondônia'
        RR = 'RR', 'Roraima'
        SC = 'SC', 'Santa Catarina'
        SP = 'SP', 'São Paulo'
        SE = 'SE', 'Sergipe'
        TO = 'TO', 'Tocantins'

    cep = models.CharField(max_length=8)
    street = models.CharField(max_length=255, verbose_name="nome_da_rua")
    number = models.CharField(max_length=10, verbose_name="numero_casa")
    city = models.CharField(max_length=255, verbose_name="cidade")
    uf = models.CharField(
        max_length=2,
        choices=UF_Choices.choices,
        default=UF_Choices.PB
    )
    address_2 = models.CharField(
        max_length=255,
        verbose_name="complemento",
        blank=True,
        null=True
    )
    reference_point = models.CharField(
        max_length=255,
        verbose_name="ponto_referencia",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Endereco'
        verbose_name_plural = 'Enderecos'

    def __str__(self):
        return str(
            f"Rua: {self.street}- Nº: {self.number} {self.city} - {self.uf}"
        )
