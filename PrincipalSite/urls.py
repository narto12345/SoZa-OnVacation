from django.urls import path
from . import views

urlpatterns = [
    path("", views.initial_page, name="initial_page"),
    path("login/", views.login, name="login"),
    path("contact/", views.contact, name="contact"),
    path("offers/", views.offers, name="offers"),
]
