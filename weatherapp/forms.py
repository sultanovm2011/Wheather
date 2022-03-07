from ajax_select.fields import AutoCompleteSelectMultipleField
from cities_light.models import City
from .models import Cities

from django import forms

class DocumentForm(forms.ModelForm):

    class Meta:
        model = Cities
        fields = ('city',)


class CoordForm(forms.ModelForm):

    class Meta:
        model = Cities
        fields = ('Latitude', 'Longitude',)


class CityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ('display_name', 'latitude', 'longitude',)
