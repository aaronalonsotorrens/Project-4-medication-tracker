from allauth.account.forms import SignupForm
from django import forms
from .models import Medication, SideEffect, UserProfile


class SideEffectForm(forms.ModelForm):
    class Meta:
        model = SideEffect
        fields = ['category', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Describe any side effects you are experiencing...'
            }),
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


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, label='Gender')
    age = forms.IntegerField(min_value=0, label='Age')
    country = forms.CharField(max_length=100, label='Country')

    def save(self, request):
        # Save the user instance
        user = super(CustomSignupForm, self).save(request)

        # Save UserProfile fields
        UserProfile.objects.create(
            user=user,
            gender=self.cleaned_data['gender'],
            age=self.cleaned_data['age'],
            country=self.cleaned_data['country'],
        )

        # Save additional user info
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        return user