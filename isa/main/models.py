from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

class Review(models.Model):
    title = models.CharField(max_length=200, default="Title")
    text = models.CharField(max_length=200, default="Body")
    score = models.FloatField(default=0) 
    poster = models.ForeignKey(Users, related_name='poster',on_delete=models.CASCADE)
    postee = models.ForeignKey(Users, related_name='postee',on_delete=models.CASCADE)