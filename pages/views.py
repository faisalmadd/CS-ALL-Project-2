from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import RegistrationForm


# Create your views here.
def homepage_view(request, *args, **kwargs):
    return render(request, "home.html", {})


def register_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Hi {user}, your account was created successfully!')
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, "register.html", {'form': form})


def login_view(request, *args, **kwargs):
    return render(request, "login.html", {})


def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})
