from django.db import models

# Create your models here.
class ItemModel(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField(null=True, blank=True, default=0)
    stock = models.IntegerField(null=True, blank=True, default=0)
    images = models.ImageField(upload_to='')

class CartModel(models.Model):
    customerId = models.IntegerField(null=True, blank=True, default=0)
    itemId = models.IntegerField(null=True, blank=True, default=0)
    itemName = models.CharField(max_length=100)
    itemValue = models.IntegerField(null=True, blank=True, default=0)
    numberOfItem = models.IntegerField(null=True, blank=True, default=0)

class SalesModel(models.Model):
    itemId = models.IntegerField(null=True, blank=True, default=0)
    numberOfItem = models.IntegerField(null=True, blank=True, default=0)
    sales = models.IntegerField(null=True, blank=True, default=0)
    date = models.CharField(max_length=100)