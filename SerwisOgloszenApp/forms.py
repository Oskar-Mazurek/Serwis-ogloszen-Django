from django import forms
from django.forms import ModelForm

from .models import *


class CustomerForm(ModelForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = Customer
        exclude = ('user', 'userType')
        labels = {
            'name': 'Imię',
            'surName': 'Nazwisko',
            'telNum': 'Numer telefonu',
            'street': 'Ulica',
            'city': 'Miasto',
            'zipCode': 'Kod pocztowy'
        }
        prefix = 'customerForm'
