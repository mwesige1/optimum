from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import AuditUser, Firm


# ============================================================
# LoginForm
# ============================================================
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })
    )


# ============================================================
# RegisterForm
# ============================================================
class RegisterForm(forms.ModelForm):
    registration_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your firm registration code',
        }),
        help_text='Ask your firm administrator for this code.'
    )
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
        model  = AuditUser
        fields = ['first_name', 'last_name', 'username', 'email', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name':  forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
            'username':   forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
            'email':      forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'role':       forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_registration_code(self):
        code = self.cleaned_data.get('registration_code')
        try:
            Firm.objects.get(registration_code=code)
        except Firm.DoesNotExist:
            raise forms.ValidationError(
                'Invalid registration code. Please check with your administrator.'
            )
        return code

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if AuditUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'This username is already taken. Please choose another.'
            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if AuditUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'An account with this email already exists.'
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        code = self.cleaned_data.get('registration_code')
        firm = Firm.objects.get(registration_code=code)
        user.firm = firm
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user