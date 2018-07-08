from django import forms
from django.forms import ModelForm, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Dishes


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Requis. Eentrez une adresse email valide.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )