##En este archivo vamos a crear todas las clases de los formularios que necesitemos (lo busqué en internet jaja)
from django import forms
from .models import Contact, Offer, OfferType


##Clase para el formulario de contacto
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control p-4",
                    "placeholder": "Escribe aquí tú nombre",
                    "required": "required",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control p-4",
                    "placeholder": "Tú email",
                    "required": "required",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control p-4",
                    "placeholder": "Asunto",
                    "required": "required",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control p-4",
                    "rows": 6,
                    "placeholder": "Mensaje",
                    "required": "required",
                }
            ),
        }
