from django import forms
from apps.clientes.models import Client
from apps.core.models import Address

class ClientForm(forms.Form):
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