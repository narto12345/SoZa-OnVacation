from datetime import datetime, timezone
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from PrincipalSite.models import *

import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings

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
            return redirect("initial_page")
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
    if request.method == "POST":
        name_request = request.POST["name"]
        description_request = request.POST["description"]
        detail_request = request.POST["detail"]
        offer_type_id = request.POST["offer_type"]

        try:
            offer_type_object = OfferType.objects.get(id=offer_type_id)
        except OfferType.DoesNotExist:
            messages.error(request, "El tipo de oferta no existe")
            return redirect("create_offer")

        gallery_images = request.FILES.getlist("galery_image")
        main_image = request.FILES.get("main_image")

        # Validar los campos
        if not all(
            [
                name_request,
                description_request,
                detail_request,
                offer_type_object,
                main_image,
                gallery_images,
            ]
        ):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect("create_offer")

        path_relative = os.path.join("img", "offers", "main")
        upload_path = os.path.join(settings.PRINCIPAL_SITE_MEDIA_ROOT, path_relative)

        fs = FileSystemStorage(location=upload_path)
        filename = fs.save(main_image.name, main_image)

        main_image_entity = MainImage(name=filename, path=path_relative)
        main_image_entity.save()

        oferta = Offer(
            name=name_request,
            description=description_request,
            offer_type=offer_type_object,
            detail=detail_request,
            main_image=main_image_entity,
        )
        oferta.save()

        path_relative_gallery = os.path.join("img", "offers", "gallery")
        upload_path_gallery = os.path.join(
            settings.PRINCIPAL_SITE_MEDIA_ROOT, path_relative_gallery
        )
        fs_gallery = FileSystemStorage(location=upload_path_gallery)

        for gallery_image in gallery_images:
            filename_gallery = fs_gallery.save(gallery_image.name, gallery_image)

            gallery_image_entity = GaleryImage(
                offer=oferta,
                name=filename_gallery,
                path=path_relative_gallery,
            )
            gallery_image_entity.save()

        messages.success(request, "¡Oferta creada con éxito!")
        return redirect("create_offer")
    else:
        return render(request, "form_offer.html")


def offer_detail(request):
    return render(request, "offer-detail.html")


@session_required
def offers_admin(request):
    offers_admin = Offer.objects.all()
    return render(request, "offers_admin.html", {"offers": offers_admin})
