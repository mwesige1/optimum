from django import forms
from .models import Engagement, EngagementMember
from apps.accounts.models import AuditUser
from apps.clients.models import AuditClient


class EngagementForm(forms.ModelForm):
    class Meta:
        model  = Engagement
        fields = [
            'name', 'client', 'audit_type', 'financial_year',
            'status', 'start_date', 'end_date',
            'lead_auditor', 'materiality', 'notes'
        ]
        widgets = {
            'name':           forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. FY2024 Annual Audit'}),
            'client':         forms.Select(attrs={'class': 'form-select'}),
            'audit_type':     forms.Select(attrs={'class': 'form-select'}),
            'financial_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. FY2024'}),
            'status':         forms.Select(attrs={'class': 'form-select'}),
            'start_date':     forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date':       forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lead_auditor':   forms.Select(attrs={'class': 'form-select'}),
            'materiality':    forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'notes':          forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # we pass the current user's firm so dropdowns only show
        # clients and users from the same firm
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['lead_auditor'].queryset = AuditUser.objects.filter(
                firm=self.user.firm, is_active=True
            )