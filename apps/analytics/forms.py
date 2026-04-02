from django import forms
from .models import RatioAnalysis, MaterialityCalculation


# ============================================================
# MaterialityForm
# Used to calculate materiality for an engagement
# ============================================================
class MaterialityForm(forms.ModelForm):
    class Meta:
        model  = MaterialityCalculation
        fields = [
            'basis', 'basis_amount', 'materiality_percentage',
            'performance_pct', 'trivial_pct', 'justification'
        ]
        widgets = {
            'basis':                  forms.Select(attrs={
                                          'class': 'form-select'
                                      }),
            'basis_amount':           forms.NumberInput(attrs={
                                          'class': 'form-control',
                                          'placeholder': 'e.g. 500000000000'
                                      }),
            'materiality_percentage': forms.NumberInput(attrs={
                                          'class': 'form-control',
                                          'placeholder': 'e.g. 5',
                                          'step': '0.01'
                                      }),
            'performance_pct':        forms.NumberInput(attrs={
                                          'class': 'form-control',
                                          'placeholder': 'e.g. 75',
                                          'step': '0.01'
                                      }),
            'trivial_pct':            forms.NumberInput(attrs={
                                          'class': 'form-control',
                                          'placeholder': 'e.g. 5',
                                          'step': '0.01'
                                      }),
            'justification':          forms.Textarea(attrs={
                                          'class': 'form-control',
                                          'rows': 3,
                                          'placeholder': 'Explain the basis and percentage chosen...'
                                      }),
        }


# ============================================================
# RatioAnalysisForm
# Used to add a financial ratio for comparison
# ============================================================
class RatioAnalysisForm(forms.ModelForm):
    class Meta:
        model  = RatioAnalysis
        fields = [
            'ratio_name', 'category', 'unit',
            'current_year_value', 'prior_year_value',
            'explanation', 'requires_followup'
        ]
        widgets = {
            'ratio_name':          forms.TextInput(attrs={
                                       'class': 'form-control',
                                       'placeholder': 'e.g. Gross Profit Margin'
                                   }),
            'category':            forms.Select(attrs={
                                       'class': 'form-select'
                                   }),
            'unit':                forms.TextInput(attrs={
                                       'class': 'form-control',
                                       'placeholder': 'e.g. % or UGX or times'
                                   }),
            'current_year_value':  forms.NumberInput(attrs={
                                       'class': 'form-control',
                                       'step': '0.01',
                                       'placeholder': 'Current year value'
                                   }),
            'prior_year_value':    forms.NumberInput(attrs={
                                       'class': 'form-control',
                                       'step': '0.01',
                                       'placeholder': 'Prior year value'
                                   }),
            'explanation':         forms.Textarea(attrs={
                                       'class': 'form-control',
                                       'rows': 3,
                                       'placeholder': 'Explain the movement between years...'
                                   }),
            'requires_followup':   forms.CheckboxInput(attrs={
                                       'class': 'form-check-input'
                                   }),
        }