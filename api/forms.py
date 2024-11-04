from django import forms
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from app import settings
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


class DeliveryTransactionFormInline(forms.ModelForm):
    name = forms.CharField(max_length=255, required=False)
    length = forms.FloatField(required=False, validators=[MinValueValidator(0)])
    width = forms.FloatField(required=False, validators=[MinValueValidator(0)])
    height = forms.FloatField(required=False, validators=[MinValueValidator(0)])
    weight = forms.FloatField(required=False, validators=[MinValueValidator(0)])
    description = forms.CharField(max_length=500, required=False)

    class Meta:
        model = DeliveryItem
        fields = ['name', 'length', 'width', 'height', 'weight', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter delivery item name'})
        self.fields['length'].widget.attrs.update({'placeholder': 'Length (in meters)'})
        self.fields['width'].widget.attrs.update({'placeholder': 'Width (in meters)'})
        self.fields['height'].widget.attrs.update({'placeholder': 'Height (in meters)'})
        self.fields['weight'].widget.attrs.update({'placeholder': 'Weight (in kg)'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Description'})
