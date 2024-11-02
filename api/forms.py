from django import forms
from .models import PersonalInformation


class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        fields = [
            'first_name', 'last_name', 'email_address', 'phone_number', 'date_of_birth',
            'gender', 'mailing_address', 'mailing_address_two', 'city', 'state', 'zip_code',
            'password', 'user_type'
        ]
        widgets = {
            'password': forms.PasswordInput(),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
