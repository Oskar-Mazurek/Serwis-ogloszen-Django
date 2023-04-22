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


class AdForm(ModelForm):
    class Meta:
        model = Ad
        exclude = ('customer', 'publicationDate', 'expirationDate')
        labels = {'adName': 'Tytuł ogłoszenia', 'description': 'Opis'}


class AdEditForm(ModelForm):
    class Meta:
        model = Ad
        exclude = ('customer', 'publicationDate', 'expirationDate', '')
        labels = {'adName': 'Tytuł ogłoszenia', 'description': 'Opis'}
