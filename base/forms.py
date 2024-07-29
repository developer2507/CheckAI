from django import forms
from .models import File

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'})
        }

class StatusUpdateForm(forms.Form):
    STATUS_CHOICES = [('S', 'Student'), ('T', 'Teacher')]
    status = forms.ChoiceField(choices=STATUS_CHOICES)
