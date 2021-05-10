from django.db import  models
from django.core.validators import MinLengthValidator

class Aadharcard(models.Model):
    aadhar_card_no = models.CharField(max_length=20)





