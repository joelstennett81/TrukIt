from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import *


class TrukItUserForm(forms.ModelForm):
    class Meta:
        model = TrukItUser
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth',
            'gender', 'mailing_address', 'city', 'state', 'zip_code',
            'password', 'user_type'
        ]
        widgets = {
            'password': forms.PasswordInput(),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class DeliveryTransactionForm(forms.ModelForm):
    request_pickup_timestamp = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'],
                                                   label='When do you want this to be picked up?',
                                                   widget=forms.DateTimeInput(attrs={
                                                       'type': 'datetime-local',
                                                       'placeholder': 'YYYY-MM-DDTHH:MM'
                                                   }))
    request_delivery_timestamp = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'],
                                                     label='When do you want this delivered?',
                                                     widget=forms.DateTimeInput(attrs={
                                                         'type': 'datetime-local',
                                                         'placeholder': 'YYYY-MM-DDTHH:MM'
                                                     }))

    class Meta:
        model = DeliveryTransaction
        fields = ['pickup_location_address', 'delivery_location_address', 'request_pickup_timestamp',
                  'request_delivery_timestamp']


class DeliveryItemForm(forms.ModelForm):
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 1}))

    class Meta:
        model = DeliveryItem
        fields = ['name', 'length', 'width', 'height', 'weight', 'description']


class DeliveryEquipmentForm(forms.Form):
    equipment = forms.ModelMultipleChoiceField(
        queryset=DeliveryEquipment.objects.all(),
        widget=FilteredSelectMultiple("Equipment", is_stacked=False),
        required=False
    )
    quantity = forms.IntegerField(min_value=0, required=False)
