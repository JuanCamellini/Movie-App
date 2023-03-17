from django import forms

class MovieFilterForm(forms.Form):
    name = forms.CharField()