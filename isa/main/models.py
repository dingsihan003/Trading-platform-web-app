from django.db import models
from datetime import datetime

# Create your models here.
class Authenticator(models.Model):
    username = models.CharField(max_length=100)
    authenticator = models.CharField(max_length=300)
    date_created = models.DateTimeField()

class Users(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    password = models.CharField(max_length=500)

class Product(models.Model):
    product_title = models.CharField(max_length=200)
    product_base_price = models.DecimalField(max_digits=12, decimal_places=2)
    product_description = models.TextField()
    product_date_added = models.DateTimeField(default=datetime.now, blank=True)
    sold = models.BooleanField(default=False)

class Review(models.Model):
    title = models.CharField(max_length=200, default="title")
    text = models.CharField(max_length=200, default="text")
    poster = models.ForeignKey(Users, related_name='poster',on_delete=models.CASCADE)
    postee = models.ForeignKey(Users, related_name='postee',on_delete=models.CASCADE)
    review_date_added = models.DateTimeField(default=datetime.now, blank=True)
