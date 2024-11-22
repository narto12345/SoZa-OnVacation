from django.db import models
"""
Nota Angie: Aquí se crearán los modelos que serán creados en la bd
"""
# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200)

