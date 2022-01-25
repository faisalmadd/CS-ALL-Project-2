from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def homepage_view(request, *args, **kwargs):
    return render(request, "home.html", {})


def contact_view(*args, **kwargs):
    return HttpResponse("<h1>Contact Page</h1>")
