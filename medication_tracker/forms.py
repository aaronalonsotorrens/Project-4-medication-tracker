from django import forms
from .models import SideEffect

class SideEffectForm(forms.ModelForm):
    class Meta:
        model = SideEffect
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Describe any side effects you are experiencing...'}),
        }