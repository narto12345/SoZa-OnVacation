from django.shortcuts import render
from django.http import HttpResponse


def initial_page(request):
    return render(request, "index.html")


def login(request):
    return render(request, "login.html")


def contact(request):
    return render(request, "contact.html")


def offers(request):
    return render(request, "offers.html")
