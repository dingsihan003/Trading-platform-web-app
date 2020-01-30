from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    location = models.CharField(max_length=50)