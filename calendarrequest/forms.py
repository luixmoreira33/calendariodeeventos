from django import forms
from .models import UserRequest
from setup.models import Profession

class UserRequestForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(
        required=True,
        label='Autorizo compartilhar minhas informações com a plataforma',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={'required': 'Você precisa aceitar os termos para continuar.'}
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the profession field
        self.fields['profession'].queryset = Profession.objects.filter(is_active=True).order_by('name')
        self.fields['profession'].empty_label = "Selecione sua profissão"

    class Meta:
        model = UserRequest
        fields = ['name', 'surname', 'email', 'phone', 'profession', 'lodge_name', 'lodge_number', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu telefone'}),
            'profession': forms.Select(attrs={'class': 'form-control'}),
            'lodge_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da sua loja'}),
            'lodge_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o número da sua loja'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite uma mensagem (opcional)', 'required': False}),
        }
