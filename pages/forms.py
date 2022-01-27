from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    contact = forms.DecimalField()

    class Meta:
        model = User
        fields = ['username', 'email', 'contact', 'password1', 'password2']