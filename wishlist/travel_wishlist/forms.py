from django import forms
from .models import Place

# Class to create a form object that will map the inputs to the database columns
class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = {'name', 'visited'} # Desired fields to be displayed


class DateInput(forms.DateInput):
    input_type = 'date'


class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = {'notes', 'date_visited', 'photo'}
        widgets = {
            'date_visited': DateInput()  # Use custom date input
        }