from django.db import models
from django import forms

# Create your models here.    
class Movie(models.Model):
    title = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.title