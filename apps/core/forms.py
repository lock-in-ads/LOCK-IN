from django import forms
from apps.administrativo.models import Enterprise, Card, Locker
from apps.clientes.models import Client
from apps.core.models import Address

class LockerForm(forms.Form):
    available = forms.BooleanField(
        required=False,
        initial=True,
        label="Disponibilidade pra uso",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )  
    number = forms.IntegerField(
        label="Número do Armário",
        min_value=0, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nº do armário'})
    )
    card = forms.ModelChoiceField(
        required=False,
        queryset=Card.objects.all(),
        label="Atribuir Cartão Chave",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    enterprise = forms.ModelChoiceField(
        queryset=Enterprise.objects.all(),
        label="Empresa:",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
class LockerAssignmentForm(forms.Form):
    available = forms.BooleanField(
        required=False, 
        initial=True, 
        label="Disponibilidade pra uso",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )  
    number = forms.IntegerField(
        required=False,
        label="Número do Armário",
        min_value=1, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'disabled': 'disabled', 'readonly': 'readonly'})
    )
    card = forms.ModelChoiceField(
        queryset=Card.objects.all(),
        required=False,
        label="Atribuir Cartão Chave",
        widget=forms.Select(attrs={'class': 'form-select', 'disabled': 'disabled', 'readonly': 'readonly'})
    )
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        label="Atribuir Usuário:",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class UserForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="Nome Completo:",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )  
    phone = forms.RegexField(
        label="Telefone",
        regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',        
        max_length=15,
        error_messages={'invalid': 'Informe um número de telefone válido.'},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(99) 99999-9999'})
    )
    email = forms.EmailField(
        label="E-mail:",
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'})
    )   
    access_level = forms.ChoiceField(
        choices=Client.LevelChoices.choices,
        label="Nível de acesso:",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    cep = forms.RegexField(
        regex=r'^\d{8}$',
        label="CEP:",
        error_messages={
            'invalid': 'Informe um CEP válido com 8 dígitos, sem o hífen.'
        },
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sem o hífen'})
    )
    street = forms.CharField(
        max_length=255, 
        label="Nome da rua:",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    number = forms.CharField(  
        max_length=10,
        label="Número:",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    city = forms.CharField(
        max_length=255, 
        label="Cidade:",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )    
    uf = forms.ChoiceField(
        choices=Address.UF_Choices.choices,
        label="Estado (UF):",
        widget=forms.Select(attrs={'class': 'form-select'})
    )    
    address_2 = forms.CharField(
        required=False,
        max_length=255,
        label="Complemento:",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )    
    reference_point = forms.CharField(
        required=False,
        max_length=255,
        label="Ponto de referência",        
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    