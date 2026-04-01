from django import forms
from .models import Workpaper, WorkpaperFile


# ============================================================
# WorkpaperForm
# Used to create and edit workpapers
# ============================================================
class WorkpaperForm(forms.ModelForm):
    class Meta:
        model  = Workpaper
        fields = [
            'reference', 'title', 'section',
            'status', 'description', 'review_comments'
        ]
        widgets = {
            'reference':       forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'e.g. WP-2100'
                               }),
            'title':           forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'e.g. Cash and Bank Procedures'
                               }),
            'section':         forms.Select(attrs={'class': 'form-select'}),
            'status':          forms.Select(attrs={'class': 'form-select'}),
            'description':     forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'rows': 6,
                                    'placeholder': 'Document the audit procedures performed, evidence obtained and conclusions reached...'
                               }),
            'review_comments': forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'rows': 3,
                                    'placeholder': 'Reviewer comments...'
                               }),
        }


# ============================================================
# WorkpaperFileForm
# Used to upload file attachments to a workpaper
# ============================================================
class WorkpaperFileForm(forms.ModelForm):
    class Meta:
        model  = WorkpaperFile
        fields = ['file', 'filename']
        widgets = {
            'file':     forms.FileInput(attrs={'class': 'form-control'}),
            'filename': forms.TextInput(attrs={
                            'class': 'form-control',
                            'placeholder': 'Display name for this file (optional)'
                        }),
        }