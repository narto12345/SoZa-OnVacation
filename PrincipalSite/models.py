from django.db import models

"""
Nota Angie: Aquí se crearán los modelos que serán creados en la bd
"""


# Create your models here.
class OfferType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SliderImage(models.Model):
    name = models.CharField(max_length=255)
    slogan = models.TextField(blank=True, null=True)
    path = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class MainImage(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class GaleryImage(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Offer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    offer_type = models.ForeignKey(OfferType, on_delete=models.CASCADE)
    slider_image = models.OneToOneField(
        SliderImage, on_delete=models.SET_NULL, null=True, blank=True
    )
    main_image = models.OneToOneField(
        MainImage, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
