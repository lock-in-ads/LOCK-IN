from django import forms
from apps.administrativo.models import Enterprise, Card, Locker
from apps.clientes.models import Client

class LockerAddForm(forms.Form):
    available = forms.BooleanField(
        required=False, 
        initial=True,
        label="Disponibilidade pra uso",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
        )  
    number = forms.IntegerField(
        required=True,
        label="Número do Armário",
        min_value=0, 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    card = forms.ModelChoiceField(
        queryset=Card.objects.all(),
        required=True,
        label="Atribuir Cartão Chave",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    enterprise = forms.ModelChoiceField(
        queryset=Enterprise.objects.all(),
        required=True,
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
        min_value=0, 
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
        required=True,
        label="Atribuir Usuário:",
        widget=forms.Select(attrs={'class': 'form-select'})
    )