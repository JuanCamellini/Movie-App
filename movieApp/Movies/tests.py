from django.test import TestCase
from .models import Top250Movies, Movies

# Create your tests here.

""" class TestModels(TestCase):
    def test_top250movies_title(self):
        top250movies = Top250Movies.objects.get(id=1)
        field_label = top250movies._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')
        
    def test_top250movies_year(self):
        top250movies = Top250Movies.objects.get(id=1)
        field_label = top250movies._meta.get_field('year').verbose_name
        self.assertEquals(field_label, 'year')
        
    def test_top250movies_image(self):
        top250movies = Top250Movies.objects.get(id=1)
        field_label = top250movies._meta.get_field('image').verbose_name
        self.assertEquals(field_label, 'image')
        
    def test_top250movies_crew(self):
        top250movies = Top250Movies.objects.get(id=1)
        field_label = top250movies._meta.get_field('crew').verbose_name
        self.assertEquals(field_label, 'crew')
        
    def test_top250movies_rating(self):
        top250movies = Top250Movies.objects.get(id=1)
        field_label = top250movies._meta.get_field('rating').verbose_name
        self.assertEquals(field_label, 'rating')
        
    def test_top250movies_genre(self):
        top250movies = Top250Movies.objects.get(id=1)
        field_label = top250movies._meta.get_field('genre').verbose_name
        self.assertEquals(field_label, 'genre')
        
    

 """