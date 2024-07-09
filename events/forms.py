from django import forms
from django.forms import ModelForm
from . models import Venue


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'phone', 'email_address')
        labels = {
             'name':'',
            'address':'',
            'phone':'',
            'email_address':'',
        }

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue Name'}),
            'address':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
            'phone':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),
            'email_address':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
        }