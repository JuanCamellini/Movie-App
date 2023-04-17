from django import forms

class MoviesFilterForm(forms.Form):
    name = forms.CharField()