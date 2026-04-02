from django import forms
from django.contrib.auth.hashers import check_password
from .models import ClientUser


# ============================================================
# ClientRegistrationForm
# Client self-registers — no firm code needed
# Partner approves them after registration
# ============================================================
class ClientRegistrationForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
        })
    )

    class Meta:
        model  = ClientUser
        fields = [
            'company_name', 'contact_person',
            'email', 'phone'
        ]
        widgets = {
            'company_name':   forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Your company name e.g. Nile Breweries Uganda'
                              }),
            'contact_person': forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Your full name'
                              }),
            'email':          forms.EmailInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'your@company.com'
                              }),
            'phone':          forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': '+256 ...'
                              }),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# ============================================================
# ClientLoginForm
# ============================================================
class ClientLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@company.com',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })
    )


# ============================================================
# ClientProfileForm
# Client updates their contact info
# ============================================================
class ClientProfileForm(forms.ModelForm):
    class Meta:
        model  = ClientUser
        fields = ['company_name', 'contact_person', 'email', 'phone']
        widgets = {
            'company_name':   forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'email':          forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':          forms.TextInput(attrs={'class': 'form-control'}),
        }


# ============================================================
# ClientChangePasswordForm
# ============================================================
class ClientChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        pwd = self.cleaned_data.get('current_password')
        if not self.user.check_password(pwd):
            raise forms.ValidationError('Current password is incorrect.')
        return pwd

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password1')
        p2 = cleaned_data.get('new_password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('New passwords do not match.')
        return cleaned_data