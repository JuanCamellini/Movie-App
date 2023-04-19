from django import forms

class SeriesFilterForm(forms.Form):
    name = forms.CharField()