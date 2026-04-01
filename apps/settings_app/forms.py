from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from apps.accounts.models import AuditUser, Firm


# ============================================================
# ProfileForm — edit personal info
# ============================================================
class ProfileForm(forms.ModelForm):
    class Meta:
        model  = AuditUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+256 ...'}),
            'avatar':     forms.FileInput(attrs={'class': 'form-control'}),
        }


# ============================================================
# ChangePasswordForm — extends Django's built-in form
# ============================================================
class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add Bootstrap classes to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# ============================================================
# FirmForm — edit firm profile (partners only)
# ============================================================
class FirmForm(forms.ModelForm):
    class Meta:
        model  = Firm
        fields = ['name', 'email', 'phone', 'address', 'logo']
        widgets = {
            'name':    forms.TextInput(attrs={'class': 'form-control'}),
            'email':   forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':   forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'logo':    forms.FileInput(attrs={'class': 'form-control'}),
        }