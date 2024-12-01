from django.urls import path
from . import views

urlpatterns = [
    path("", views.InitialPage),
    # path("", views.Login, name="index"),
    path("login/", views.Login, name="login"),
    path('contact/',views.Contact, name='contact')
]
