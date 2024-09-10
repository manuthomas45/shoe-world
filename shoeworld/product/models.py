from django.db import models
from categoryy.models import Category
from brand.models import Brand
from account.models import User

# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length=50)
    product_description = models.CharField(max_length=700)
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    product_brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    offer_price = models.DecimalField(max_digits=8, decimal_places=2)
    thumbnail = models.ImageField(upload_to='thumbnail_images', null=True)
    
    is_active = models.BooleanField(default=False)
    created_at = models.BooleanField(null=True,default=True)
    updated_at = models.BooleanField(null=True,default=True)
    
    def percentage_discount(self):
        return int(((self.price - self.offer_price) / self.price) * 100)
    
    def __str__(self):
        return self.product_name
    

class ProductVariant(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    size = models.CharField(max_length=8, null=True)
    variant_stock = models.PositiveIntegerField(null=False,default=0)
    variant_status = models.BooleanField(default=True)
    
    
class ProductImages(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    images = models.ImageField(
        upload_to='product_images', default=""
    )
    
    def __str__(self):      
        return f"Image for{self.product.product_name}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='reviews',  on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.CharField( max_length=50)
    
    created_at = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return f'{self.user} - {self.product}'
