from datetime import datetime, timezone
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse

from PrincipalSite.models import *
from .forms import ContactForm

ADMIN_USER = "admin"
ADMIN_PASSWORD = "contrasena"


def session_required(view_func):
    """
    Decorador para proteger vistas basadas en sesión.
    Redirige al login si no está autenticado.
    """

    def wrapper(request, *args, **kwargs):
        if not request.session.get("is_authenticated", False):
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return wrapper


def initial_page(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == ADMIN_USER and password == ADMIN_PASSWORD:
            request.session["is_authenticated"] = True
            return redirect("initial_page")  # Cambiar por la vista principal
        return render(
            request, "login.html", {"error": "Usuario o contraseña incorrectos"}
        )
    return render(request, "login.html")


def logout_view(request):
    request.session.flush()
    return redirect("initial_page")


def contact(request):
    # Se debe generar la variable form para cualquier petición, sea post o get
    form = ContactForm()  # Se usa vacía por si el valor es un get.

    if request.method == "POST":
        form = ContactForm(
            request.POST
        )  # Se obtienen los datos del formulario y se guardan

        if (
            form.is_valid()
        ):  # Esta parte es propia de django, lo usamos para que valide campos obligatorios y demás
            # Crear un nuevo objeto Contact con los datos que envió el usuario.
            contact = Contact(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                subject=form.cleaned_data["subject"],
                message=form.cleaned_data["message"],
                created_at=datetime.now(),
            )

            # Guardar el objeto Contact en la base de datos y en el modelo que se creó
            contact.save()

            # Devolver una respuesta JSON de éxito (para que active el modal)
            return JsonResponse({"success": True})

        else:
            # Si el formulario no es válido, devolver los errores
            return JsonResponse({"success": False, "errors": form.errors})

    # Si la solicitud no es POST (es un GET o algún otro tipo), se renderiza para que pueda ver la página habitual
    return render(request, "contact.html", {"form": form})


def offers(request):
    return render(request, "offers.html")


@session_required
def trazability(request):
    contacts = (
        Contact.objects.all()
    )  ##Lo usamos para traer todos los datos del modelo y plasmarlos posteriormente en la tabla :)
    return render(request, "trazability.html", {"contacts": contacts})


@session_required
def create_offer(request):
    return render(request, "form_offer.html")


def offer_detail(request):
    return render(request, "offer-detail.html")


@session_required
def offers_admin(request):
    offers_admin = Offer.objects.all()
    return render(request, "offers_admin.html", {"offers": offers_admin})
