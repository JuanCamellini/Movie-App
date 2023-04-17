from django.db import models
from django.conf import settings

# Create your models here.

class BaseMediaModel(models.Model):
    """ Comparte estilo base model.
    
    BaseMediaModel acts as an abstract base class from which every other model in
    the project will inherit. This class provides every table with the following
    attributes:
        + title - CharField
        + year - CharField
        + image - CharField
        + crew - CharField
        + rating - FloatField
        + genre - CharField
    """
    title = models.CharField(max_length=250, null=True, unique=True)
    year = models.CharField(max_length=255,null=True)
    image = models.CharField(max_length=200, null=True)
    crew = models.CharField(max_length=200, null=True)
    rating = models.FloatField(max_length=10, null=True)
    genre = models.CharField(max_length= 127, null=True)
    
    class Meta:
        abstract = True
        
class Top250Movies(BaseMediaModel):
    rank = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.title} ({self.year})"
    
    class Meta:
        verbose_name_plural = "Top 250 Movies"

class Movies(BaseMediaModel):
    plot = models.CharField(max_length=255, null=True)
    director = models.CharField(max_length=127, null=True)
    duration = models.CharField(max_length=127, null=True)
    movie_id = models.CharField(max_length=44, null=True)

    def __str__(self):
        return f"{self.title} ({self.year})"
    
    class Meta:
        verbose_name_plural = "Movies"

class MoviesLiked(models.Model):
    movie_id = models.ForeignKey(Movies, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.movie_id.title} liked by {self.user_id.username}"
    
    class Meta:
        verbose_name_plural = "Movies Liked"
