from django.db import models

from django.db import models
from django.contrib.auth.models import User,auth

class Category(models.Model):
    category_name = models.CharField(max_length=100)

class Product(models.Model):
    categoryf_name = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    product_name = models.CharField(max_length=100)
    product_price = models.IntegerField(null=True)
    product_description = models.CharField(max_length=250)
    product_image = models.ImageField(null=True,upload_to="image/")
    
class Customer(models.Model):
    customer_name = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_address = models.CharField(max_length=250)
    customer_number = models.IntegerField()
    customer_image = models.ImageField(null=True,upload_to="image/")
    
    
class Cart(models.Model):
    user_cart = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    user_product = models.ForeignKey(Product, on_delete=models.CASCADE, null = True)
    quantity = models.PositiveIntegerField(default=1)
    
    def total_price(self):
        return self.quantity * self.user_product.product_price  
