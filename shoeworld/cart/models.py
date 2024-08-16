from django.db import models
from account.models import *
from product.models import *

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user


class CartItem(models.Model):   
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart")
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def total(self):
        return self.product.offer_price * self.quantity

    def __str__(self):
        return self.product.product_name
