from django import forms


# ============================================================
# LoginForm
# A simple form with username and password fields
# We build it manually so we have full control over
# how it looks and behaves
# ============================================================
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',        # Bootstrap input styling
            'placeholder': 'Enter your username',
            'autofocus': True               # cursor lands here automatically on page load
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',        # Bootstrap input styling
            'placeholder': 'Enter your password',
        })
    )