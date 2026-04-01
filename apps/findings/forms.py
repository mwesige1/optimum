from django import forms
from .models import Finding, ManagementResponse


# ============================================================
# FindingForm
# Used to create and edit findings
# ============================================================
class FindingForm(forms.ModelForm):
    class Meta:
        model  = Finding
        fields = [
            'title', 'category', 'risk_level', 'status',
            'criteria', 'condition', 'cause', 'effect',
            'recommendation', 'assigned_to', 'due_date'
        ]
        widgets = {
            'title':          forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Brief title of the finding'
                              }),
            'category':       forms.Select(attrs={'class': 'form-select'}),
            'risk_level':     forms.Select(attrs={'class': 'form-select'}),
            'status':         forms.Select(attrs={'class': 'form-select'}),
            'criteria':       forms.Textarea(attrs={
                                'class': 'form-control', 'rows': 3,
                                'placeholder': 'What should be happening — the standard or control requirement'
                              }),
            'condition':      forms.Textarea(attrs={
                                'class': 'form-control', 'rows': 3,
                                'placeholder': 'What is actually happening — the problem you observed'
                              }),
            'cause':          forms.Textarea(attrs={
                                'class': 'form-control', 'rows': 3,
                                'placeholder': 'Why is this problem occurring'
                              }),
            'effect':         forms.Textarea(attrs={
                                'class': 'form-control', 'rows': 3,
                                'placeholder': 'What is the impact or risk if this is not fixed'
                              }),
            'recommendation': forms.Textarea(attrs={
                                'class': 'form-control', 'rows': 3,
                                'placeholder': 'What the client should do to fix this'
                              }),
            'assigned_to':    forms.Select(attrs={'class': 'form-select'}),
            'due_date':       forms.DateInput(attrs={
                                'class': 'form-control',
                                'type': 'date'
                              }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # only show users from the same firm in assigned_to dropdown
        if self.user:
            from apps.accounts.models import AuditUser
            self.fields['assigned_to'].queryset = AuditUser.objects.filter(
                firm=self.user.firm,
                is_active=True
            )


# ============================================================
# ManagementResponseForm
# Used by auditors to record the client's response
# ============================================================
class ManagementResponseForm(forms.ModelForm):
    class Meta:
        model  = ManagementResponse
        fields = [
            'response_type', 'response_text',
            'action_plan', 'responded_by'
        ]
        widgets = {
            'response_type':  forms.Select(attrs={'class': 'form-select'}),
            'response_text':  forms.Textarea(attrs={
                                'class': 'form-control', 'rows': 4,
                                'placeholder': 'The client\'s written response to this finding'
                              }),
            'action_plan':    forms.Textarea(attrs={
                                'class': 'form-control', 'rows': 3,
                                'placeholder': 'What will be done to fix this and by when'
                              }),
            'responded_by':   forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'e.g. John Smith — Finance Manager'
                              }),
        }