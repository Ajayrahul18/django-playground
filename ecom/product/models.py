from typing import Any
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.TextChoices):
    ELECTRONICS = 'Electronics'
    LAPTOPS = 'Laptops'
    ARTS = 'Arts'
    FOOD = 'Food'
    HOME = 'Home'
    KITCHEN = 'Kitchen'

class Product(models.Model):
    name = models.CharField(max_length=200, default='')
    description = models.TextField(max_length=500, default='')
    price = models.DecimalField(max_digits=7, default=0, decimal_places=2)
    brand = models.CharField(max_length=200, default='')
    category = models.CharField(max_length=30, choices=Category.choices)
    ratings = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="images")
    images = models.ImageField(upload_to="products")

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ratings = models.IntegerField(default=0)
    comment = models.TextField(default="", null=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment