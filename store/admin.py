from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from .models.farmer import Farmer
from .models.aadhar import Aadharcard
from .models.weatherdata import Weatherdata
from .models.farmorder import Farmorder


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']



class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


# Register your models here.
admin.site.register(Product, AdminProduct)
admin.site.register(Category , AdminCategory)
admin.site.register(Customer )
admin.site.register(Order )
admin.site.register(Farmer)
admin.site.register(Aadharcard)
admin.site.register(Weatherdata)
admin.site.register(Farmorder)
