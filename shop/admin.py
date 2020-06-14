from django.contrib import admin
from .models import ItemModel, CartModel, SalesModel

# Register your models here.
admin.site.register(ItemModel)
admin.site.register(CartModel)
admin.site.register(SalesModel)