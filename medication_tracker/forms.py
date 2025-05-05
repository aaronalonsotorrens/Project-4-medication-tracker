from django import forms
from .models import Medication, SideEffect


class SideEffectForm(forms.ModelForm):
    class Meta:
        model = SideEffect
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Describe any side effects you are experiencing...'}),
        }


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'category', 'dosage', 'frequency', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter medication name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter dosage (e.g., 500mg)'}),
            'frequency': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Times per day'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }