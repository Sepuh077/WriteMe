from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class Registration(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '  Password'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '  Password confirm'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '  Username'}),
            'email': forms.TextInput(attrs={'placeholder': '  E-mail'}),
            'first_name': forms.TextInput(attrs={'placeholder': '  First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': '  Last Name'}),
        }


# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = []
