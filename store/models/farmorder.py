from django.db import models
from .product import Product
from .farmer import Farmer
import datetime


class Farmorder(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer,
                                 on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.today)
    category1 = models.CharField(max_length=20, default='Cereals')
    

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_farmer(farmer_id):
        return Farmorder.objects.filter(farmer=farmer_id).order_by('-date')

