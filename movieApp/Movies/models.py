from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=250, null=True, unique=True)
    year = models.CharField(max_length=200, null=True)
    image = models.CharField(max_length=200, null=True)
    crew = models.CharField(max_length=200, null=True)
    rank = models.CharField(max_length=200, null=True)
    #imDbRating = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.title} ({self.year})"