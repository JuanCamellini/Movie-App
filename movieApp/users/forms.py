from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='')
    email = forms.EmailField(label='')
    password1 = forms.CharField(label='', widget=forms.PasswordInput)
    password2 = forms.CharField(label='', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'email','style':'width:600px;display:block','type':'text' ,'placeholder':"enter your username"})
        self.fields['password1'].widget.attrs.update({'class':'email', 'style':'width:600px', 'placeholder':"enter your password"})
        self.fields['password2'].widget.attrs.update({'class':'email', 'style':'width:600px' , 'placeholder':"repeat your password"})
        self.fields['email'].widget.attrs.update({'class':'email', 'style':'width:600px' ,'type':'email','placeholder':"enter your email"})
        fields = ['username', 'email', 'password1', 'password2']
        for fieldname in fields:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k: "" for k in fields}

#Form para actualizar el usuario
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Enter your new password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Enter again your password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

