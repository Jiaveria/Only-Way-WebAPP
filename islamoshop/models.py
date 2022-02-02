from django.shortcuts import reverse
from tkinter import CASCADE
from django.db import models
from datetime import datetime

# Create your models here.

class userData(models.Model):
    userID = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.TextField(max_length=100)
    phone = models.TextField(max_length=2000)




class purchasingHistory(models.Model):
    productId =  models.IntegerField()
    username = models.EmailField()
    transactionId = models.AutoField(primary_key=True)
    createdAt = models.DateTimeField(default=datetime.now)
    priceOfOneUnit = models.DecimalField(decimal_places=2, max_digits=5)
    quantityOfProduct = models.IntegerField()

class productDetails(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2,max_digits=5)
    inStock = models.BooleanField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product", kwargs={
            'id':self.id
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'id': self.id
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'id': self.id
        })

