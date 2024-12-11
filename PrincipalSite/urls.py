from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.initial_page, name="initial_page"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("contact/", views.contact, name="contact"),
    path("offers/<str:offer_type>/", views.offers, name="offers"),
    path("trazability/", views.trazability, name="trazability"),
    path("create_offer/", views.create_offer, name="create_offer"),
    path("offer-detail/<int:name_offer>/", views.offer_detail, name="offer-detail"),
    path("offers-admin/", views.offers_admin, name="offers_admin"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
