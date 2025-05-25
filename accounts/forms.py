from allauth.account.forms import SignupForm
from django import forms
from .models import UserProfile
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, label='Gender')
    age = forms.IntegerField(min_value=0, label='Age')
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(layout='{widget}'),  # Removes flag
        label='Country'
    )

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