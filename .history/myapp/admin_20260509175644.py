from django.contrib import admin
from .productModel import Product
from .profileModel import FarmerProfile

# Register your models here.
admin.site.register(Product)
admin.site.register(FarmerProfile)

