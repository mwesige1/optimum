from django import forms
from .models import AuditClient


class ClientForm(forms.ModelForm):
    class Meta:
        model  = AuditClient
        fields = [
            'name', 'industry', 'contact_person',
            'contact_email', 'contact_phone',
            'address', 'website'
        ]
        widgets = {
            'name':           forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company name'}),
            'industry':       forms.Select(attrs={'class': 'form-select'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Main contact name'}),
            'contact_email':  forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contact@company.com'}),
            'contact_phone':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+256 ...'}),
            'address':        forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'website':        forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://'}),
        }