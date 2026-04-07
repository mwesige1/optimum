from django import forms
from .models import Workpaper, WorkpaperFile


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
                                    'placeholder': 'e.g. E110',
                                    'id': 'id_reference',
                               }),
            'title':           forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Workpaper title',
                                    'id': 'id_title',
                               }),
            'section':         forms.Select(attrs={
                                    'class': 'form-select'
                               }),
            'status':          forms.Select(attrs={
                                    'class': 'form-select'
                               }),
            'description':     forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'rows': 12,
                                    'id': 'id_description',
                                    'placeholder': 'Document procedures performed...'
                               }),
            'review_comments': forms.Textarea(attrs={
                                    'class': 'form-control',
                                    'rows': 3,
                                    'placeholder': 'Reviewer comments...'
                               }),
        }


class WorkpaperFileForm(forms.ModelForm):
    class Meta:
        model  = WorkpaperFile
        fields = ['file', 'filename']
        widgets = {
            'file':     forms.FileInput(attrs={
                            'class': 'form-control'
                        }),
            'filename': forms.TextInput(attrs={
                            'class': 'form-control',
                            'placeholder': 'Display name (optional)'
                        }),
        }