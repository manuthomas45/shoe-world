from django.db import models
from account.models import *
from product.models import *
# Create your models here.



class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    house_name = models.CharField(max_length=500, null=False)
    street_name = models.CharField(max_length=500, null=False)
    pin_number = models.IntegerField(null=False)
    district = models.CharField(max_length=300, null=False)
    state = models.CharField(max_length=300, null=False)
    country = models.CharField(max_length=50, null=False, default="null")
    phone_number = models.CharField(max_length=50, null=False)
    
    status = models.BooleanField(default=False)
    order_status = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.name
    
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.first_name}'s wishlist: {self.variant}"
    


    