from django import forms
from .models import RiskArea, RiskMatrix


# ============================================================
# RiskAreaForm
# Used to assess one risk area in an engagement
# ============================================================
class RiskAreaForm(forms.ModelForm):
    class Meta:
        model  = RiskArea
        fields = [
            'area', 'custom_area_name',
            'inherent_risk', 'control_risk', 'detection_risk',
            'key_risks', 'audit_response'
        ]
        widgets = {
            'area':             forms.Select(attrs={
                                    'class': 'form-select'
                                }),
            'custom_area_name': forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Custom area name if Other selected'
                                }),
            'inherent_risk':    forms.NumberInput(attrs={
                                    'class': 'form-control',
                                    'min': 0, 'max': 100,
                                    'placeholder': '0-100'
                                }),
            'control_risk':     forms.NumberInput(attrs={
                                    'class': 'form-control',
                                    'min': 0, 'max': 100,
                                    'placeholder': '0-100'
                                }),
            'detection_risk':   forms.NumberInput(attrs={
                                    'class': 'form-control',
                                    'min': 0, 'max': 100,
                                    'placeholder': '0-100'
                                }),
            'key_risks':        forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'rows': 3,
                                    'placeholder': 'Describe the key risks in this area...'
                                }),
            'audit_response':   forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'rows': 3,
                                    'placeholder': 'What audit procedures will address these risks?'
                                }),
        }


# ============================================================
# RiskMatrixForm
# Used to set the overall engagement risk and materiality
# ============================================================
class RiskMatrixForm(forms.ModelForm):
    class Meta:
        model  = RiskMatrix
        fields = [
            'overall_risk', 'overall_materiality',
            'performance_materiality', 'materiality_basis',
            'audit_approach'
        ]
        widgets = {
            'overall_risk':             forms.Select(attrs={
                                            'class': 'form-select'
                                        }),
            'overall_materiality':      forms.NumberInput(attrs={
                                            'class': 'form-control',
                                            'placeholder': 'e.g. 50000000'
                                        }),
            'performance_materiality':  forms.NumberInput(attrs={
                                            'class': 'form-control',
                                            'placeholder': 'e.g. 37500000'
                                        }),
            'materiality_basis':        forms.TextInput(attrs={
                                            'class': 'form-control',
                                            'placeholder': 'e.g. 5% of total revenue'
                                        }),
            'audit_approach':           forms.Textarea(attrs={
                                            'class': 'form-control',
                                            'rows': 4,
                                            'placeholder': 'Describe the overall audit approach and strategy...'
                                        }),
        }