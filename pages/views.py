from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def homepage_view(request, *args, **kwargs):
    return render(request, "home.html", {})


def register_view(request, *args, **kwargs):
    return render(request, "register.html", {})


def login_view(request, *args, **kwargs):
    return render(request, "login.html", {})


def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})
