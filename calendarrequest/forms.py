from django import forms
from .models import UserRequest

class UserRequestForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(
        required=True,
        label='Autorizo compartilhar minhas informações com a plataforma',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={'required': 'Você precisa aceitar os termos para continuar.'}
    )

    class Meta:
        model = UserRequest
        fields = ['name', 'surname', 'email', 'phone', 'lodge_name', 'lodge_number', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'lodge_name': forms.TextInput(attrs={'class': 'form-control'}),
            'lodge_number': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'required': False}),
        }
