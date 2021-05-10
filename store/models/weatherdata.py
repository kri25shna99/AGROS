from django.db import  models
from django.core.validators import MinLengthValidator

class Weatherdata(models.Model):
    latitude = models.FloatField()
    phone = models.CharField(max_length=15)
    longitude = models.FloatField()





