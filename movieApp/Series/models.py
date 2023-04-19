from django.db import models
from django.conf import settings

from Movies.models import BaseMediaModel

# Create your models here.
class Series(BaseMediaModel):
    plot = models.CharField(max_length=255, null=True)
    director = models.CharField(max_length=127, null=True)
    duration = models.CharField(max_length=127, null=True)
    series_id = models.CharField(max_length=44, null=True)

    def __str__(self):
        return f"{self.title} ({self.year})"
    
    class Meta:
        verbose_name_plural = "Series"

class Top250Series(BaseMediaModel):
    rank = models.IntegerField(null=True)
    serie_id = models.CharField(max_length=44, null=True)
    ratingCount = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.title} ({self.year})"
    
    class Meta:
        verbose_name_plural = "Top 250 Series"

class SeriesLiked(models.Model):
    movie_id = models.ForeignKey(Series, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.movie_id.title} liked by {self.user_id.username}"
    
    class Meta:
        verbose_name_plural = "Series Liked"