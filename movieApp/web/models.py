from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.user
""" 
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path) """
    
class Movie(models.Model):
    title = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.title