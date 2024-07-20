from django import forms
from django.forms import ModelForm
from . models import Venue, Event


# AdminSuperUser Event Form
class EventFormAdmin(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'manager','attendees', 'description')
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'venue': 'Venue',
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': '',
        }

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
            'event_date':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Date'}),
            'venue':forms.Select(attrs={'class':'form-select', 'placeholder':'Venue'}),
            'manager':forms.Select(attrs={'class':'form-select', 'placeholder':'Manager'}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Attendees'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
        }

# UserEventForm
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'attendees', 'description')
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'venue': 'Venue',
            'attendees': 'Attendees',
            'description': '',
        }

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
            'event_date':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Date'}),
            'venue':forms.Select(attrs={'class':'form-select', 'placeholder':'Venue'}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Attendees'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
        }




class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'phone', 'email_address', 'venue_image')
        labels = {
            'name': '',
            'address': '',
            'phone': '',
            'email_address': '',
            'venue_image': ''
        }

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue Name'}),
            'address':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
            'phone':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),
            'email_address':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
        }