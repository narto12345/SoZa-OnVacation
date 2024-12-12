from datetime import datetime, timezone
import re
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import pytz
from PrincipalSite.forms import ContactForm
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
    principal_offers = Offer.objects.filter(offer_type=3)
    slider = (Offer.objects.filter(offer_type=2).order_by("id"),)
    locations = Offer.objects.filter(offer_type=4)
    image_cards = MainImage.objects.filter(offer__offer_type_id=5)
    return render(
        request,
        "index.html",
        {
            "principal_offers": principal_offers,
            "slider_data": slider,
            "locations": locations,
            "image_cards": image_cards,
        },
    )


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

    # Obtenemos con la nueva librería la zona horaria de Colombia
    colombia_tz = pytz.timezone("America/Bogota")
    # Ahora obtenemos la hora
    utc_now = datetime.utcnow()
    # Luego la convertimos a Zona colombiana
    utc_now = pytz.utc.localize(utc_now)
    colombia_time = utc_now.astimezone(colombia_tz)
    if request.method == "POST":
        form = ContactForm(
            request.POST
        )  # Se obtienen los datos del formulario y se guardan

        if (
            form.is_valid()
        ):  # Esta parte es propia de django, lo usamos para que valide campos obligatorios y demás
            # Crear un nuevo objeto Contact con los datos que envió el usuario.
            # Definir la zona horaria de Colombia

            # Asegúrate de convertirlo a la zona horaria de Colombia
            # Obtener la hora actual en UTC y luego convertirla a la hora de Colombia

            contact = Contact(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                subject=form.cleaned_data["subject"],
                message=form.cleaned_data["message"],
                # created_at=datetime.now(),
                created_at=colombia_time,
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


def offers(request, offer_type):
    if offer_type == "nacionales":
        offers_general = Offer.objects.filter(location_menu_id=1)
    elif offer_type == "internacionales":
        offers_general = Offer.objects.filter(location_menu_id=2)
    elif offer_type == "alojamientos":
        offers_general = Offer.objects.filter(location_menu_id=3)
    else:
        offers_general = Offer.objects.filter(location_menu_id=4)

    # offers_general=Offer.objects.filter(offer_type=1)
    return render(request, "offers.html", {"offers_general": offers_general})


@session_required
def trazability(request):
    contacts = Contact.objects.all()

    # Capturar los parámetros corregidos
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    # Filtrar si ambas fechas están presentes
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            contacts = contacts.filter(created_at__date__range=(start_date, end_date))
        except ValueError:
            messages.error(request, "Formato de fechas inválido.")

    return render(request, "trazability.html", {"contacts": contacts})


@session_required
def create_offer(request):
    if request.method == "POST":
        name_request = request.POST["name"]
        description_request = request.POST["description"]
        detail_request = request.POST["detail"]
        price_request = request.POST["price"]
        offer_type_id = request.POST["offer_type"]
        location_menu_id = request.POST["location_menu"]
        info_request = request.POST["moreinfo"]
        price_request = re.sub(r"\D", "", price_request)
        try:
            offer_type_object = OfferType.objects.get(id=offer_type_id)
        except OfferType.DoesNotExist:
            messages.error(request, "El tipo de oferta no existe")
            return redirect("create_offer")

        try:
            location_menu_object = LocationMenu.objects.get(id=location_menu_id)
        except LocationMenu.DoesNotExist:
            messages.error(request, "La localización no existe")
            return redirect("create_offer")

        gallery_images = request.FILES.getlist("galery_image")
        main_image = request.FILES.get("main_image")

        print("price= " + price_request)

        # Validar los campos
        if not all(
            [
                name_request,
                description_request,
                detail_request,
                price_request,
                offer_type_object,
                main_image,
                gallery_images,
                location_menu_object,
            ]
        ):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect("create_offer")

        if len(gallery_images) > 3:
            messages.error(request, "No puedes subir más de 3 imágens")
            return redirect("create_offer")

        path_relative = os.path.join("img", "offers", "main")
        upload_path = os.path.join(settings.PRINCIPAL_SITE_MEDIA_ROOT, path_relative)

        fs = FileSystemStorage(location=upload_path)
        filename = fs.save(main_image.name, main_image)

        main_image_entity = MainImage(name=filename, path=path_relative)
        main_image_entity.save()

        if offer_type_object.name == "slider":
            current_sliders = SliderImage.objects.all()
            if current_sliders.count() >= 3:
                messages.error(request, "No pueden haber más de 3 sliders")
                return redirect("create_offer")

        if offer_type_object.name == "oferta principal":
            current_offer_main = Offer.objects.filter(
                offer_type__name="oferta principal"
            )
            if current_offer_main.count() >= 3:
                messages.error(request, "No pueden haber más de 3 ofertas principales")
                return redirect("create_offer")

        if offer_type_object.name == "promocion":
            current_promotions = Offer.objects.filter(offer_type__name="promocion")
            if current_promotions.count() >= 4:
                messages.error(request, "No pueden haber más de 4 imagenes promociones")
                return redirect("create_offer")

        if offer_type_object.name == "destino principal":
            current_destination = Offer.objects.filter(
                offer_type__name="destino principal"
            )
            if current_destination.count() >= 6:
                messages.error(request, "No pueden haber más de 6 destinos principales")
                return redirect("create_offer")

        oferta = Offer(
            name=name_request,
            description=description_request,
            offer_type=offer_type_object,
            detail=detail_request,
            price=price_request,
            main_image=main_image_entity,
            location_menu=location_menu_object,
            more_information=info_request,
        )

        if offer_type_object.name == "slider":
            slider_object = SliderImage(name=name_request, slogan=detail_request)

            slider_object.save()
            oferta.slider_image = slider_object

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


@session_required
def delete_offer(request, offer_id):
    try:
        offer = Offer.objects.get(id=offer_id)
    except Offer.DoesNotExist:
        messages.error(request, "La oferta no existe")
        return redirect("offers_admin")

    # Eliminar images
    if offer.main_image:
        main_image_path = os.path.join(
            settings.PRINCIPAL_SITE_MEDIA_ROOT,
            offer.main_image.path,
            offer.main_image.name,
        )
        if os.path.exists(main_image_path):
            os.remove(main_image_path)

    gallery_images = GaleryImage.objects.filter(offer=offer)
    for gallery_image in gallery_images:
        gallery_image_path = os.path.join(
            settings.PRINCIPAL_SITE_MEDIA_ROOT, gallery_image.path, gallery_image.name
        )
        if os.path.exists(gallery_image_path):
            os.remove(gallery_image_path)
        gallery_image.delete()

    main_image = offer.main_image
    offer.delete()

    if offer.slider_image:
        slider_image = offer.slider_image
        slider_image.delete()

    main_image.delete()

    messages.success(request, "¡Oferta eliminada con éxito!")
    return redirect("offers_admin")


def offer_detail(request, name_offer):
    detail_offer = Offer.objects.filter(id=name_offer)
    gallery_images = GaleryImage.objects.filter(offer_id=name_offer)
    print(gallery_images)
    return render(
        request,
        "offer-detail.html",
        {"detail_offer": detail_offer, "gallery_images": gallery_images},
    )


@session_required
def offers_admin(request):
    offers_admin = Offer.objects.all()
    return render(request, "offers_admin.html", {"offers": offers_admin})


@session_required
def edit_offer(request, offer_id):
    try:
        offer = Offer.objects.get(id=offer_id)
    except Offer.DoesNotExist:
        messages.error(request, "La oferta no existe")
        return redirect("offers_admin")

    gallery_images = GaleryImage.objects.filter(offer=offer)
    offer_types = OfferType.objects.all()
    location_menus = LocationMenu.objects.all()

    if request.method == "POST":
        offer.name = request.POST["name"]
        offer.description = request.POST["description"]
        offer.detail = request.POST["detail"]
        offer.price = request.POST["price"]
        offer.more_information = request.POST["moreinfo"]

        offer_type_id = request.POST["offer_type"]
        location_menu_id = request.POST["location_menu"]

        try:
            offer.offer_type = OfferType.objects.get(id=offer_type_id)
        except OfferType.DoesNotExist:
            messages.error(request, "El tipo de oferta no existe")
            return redirect("edit_offer", offer_id=offer_id)

        try:
            offer.location_menu = LocationMenu.objects.get(id=location_menu_id)
        except LocationMenu.DoesNotExist:
            messages.error(request, "La localización no existe")
            return redirect("edit_offer", offer_id=offer_id)

        main_image = request.FILES.get("main_image")

        if main_image:
            # Eliminar la imagen principal anterior
            if offer.main_image:
                main_image_path = os.path.join(
                    settings.PRINCIPAL_SITE_MEDIA_ROOT,
                    offer.main_image.path,
                    offer.main_image.name,
                )
                if os.path.exists(main_image_path):
                    os.remove(main_image_path)
                offer.main_image.delete()

            # Guardar la nueva imagen principal
            path_relative = os.path.join("img", "offers", "main")
            upload_path = os.path.join(
                settings.PRINCIPAL_SITE_MEDIA_ROOT, path_relative
            )
            fs = FileSystemStorage(location=upload_path)
            filename = fs.save(main_image.name, main_image)
            main_image_entity = MainImage(name=filename, path=path_relative)
            main_image_entity.save()
            offer.main_image = main_image_entity

        # Gestionar las imágenes de galería
        new_gallery_images = request.FILES.getlist("galery_image")
        if new_gallery_images:
            # Eliminar las imágenes de galería anteriores
            for gallery_image in gallery_images:
                gallery_image_path = os.path.join(
                    settings.PRINCIPAL_SITE_MEDIA_ROOT,
                    gallery_image.path,
                    gallery_image.name,
                )
                if os.path.exists(gallery_image_path):
                    os.remove(gallery_image_path)
                gallery_image.delete()

            # Guardar las nuevas imágenes de galería
            path_relative_gallery = os.path.join("img", "offers", "gallery")
            upload_path_gallery = os.path.join(
                settings.PRINCIPAL_SITE_MEDIA_ROOT, path_relative_gallery
            )
            fs_gallery = FileSystemStorage(location=upload_path_gallery)

            for gallery_image in new_gallery_images:
                filename_gallery = fs_gallery.save(gallery_image.name, gallery_image)
                gallery_image_entity = GaleryImage(
                    offer=offer,
                    name=filename_gallery,
                    path=path_relative_gallery,
                )
                gallery_image_entity.save()

        if offer.offer_type.name == "slider":

            if offer.slider_image:
                slider = offer.slider_image
                slider.name = offer.name
                slider.slogan = offer.detail
                slider.save()
            else:
                slider_object = SliderImage(name=offer.name, slogan=offer.detail)
                slider_object.save()
                offer.slider_image = slider_object

        if offer.offer_type.name != "slider" and offer.slider_image:
            slider_image_to_delete = offer.slider_image
            offer.slider_image = None
            if slider_image_to_delete:
                slider_image_to_delete.delete()

        offer.save()
        messages.success(request, "¡Oferta actualizada con éxito!")
        return redirect("offers_admin")

    return render(
        request,
        "edit_offer.html",
        {
            "offer": offer,
            "offer_types": offer_types,
            "location_menus": location_menus,
            "gallery_images": gallery_images,
        },
    )
