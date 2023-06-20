from django.shortcuts import render, redirect
from django.db import transaction
from django.core.paginator import Paginator
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)

import django_filters 
import requests
import crispy_forms

from api_key import api_key
from .models import Top250Movies
from .filters import MoviesFilter, Top250MoviesFilter
from .forms import MoviesFilterForm

# Create your views here.

class MovieListView(ListView):
    model = Top250Movies
    template_name = 'Movies/movies-top-250.html'
    context_object_name = 'movies'
    paginate_by = 50 
    is_paginated = True

    def get_movie(request):
        if request.method == 'POST':
            movie = request.POST['movie'].lower()
            if " " in movie:
                movie.replace(" ","%20")
                url = f"https://imdb-api.com/en/API/AdvancedSearch/{api_key}/?title={movie}"
            response = requests.get(url)
            dataset = response.json()     
        try:        
            context = {
                ### 
                "id": dataset['results'][0]['id'],
                "image": dataset['results'][0]['image'],
                "title": dataset['results'][0]['title'],
                "year": dataset['results'][0]['description'],
                "duration": dataset['results'][0]['runtimeStr'],
                "genres": dataset['results'][0]['genres'],
                "rating": dataset['results'][0]['imDbRating'],
                "plot": dataset['results'][0]['plot'],
                "stars": dataset['results'][0]['stars'],
                "director":dataset['results'][0]['starList'][0]['name'],
            }
            #add the genres to the column genre in top250movies db with transaction.atomic
            with transaction.atomic():
                for genre in context['genres']:
                    Top250Movies.objects.create(
                        id = context['id'],
                        image = context['image'],
                        title = context['title'],
                        year = context['year'],
                        duration = context['duration'],
                        genre = genre,
                        rating = context['rating'],
                        plot = context['plot'],
                        stars = context['stars'],
                        director = context['director'],
                    )
        except:
            context = { 
                "error": "Movie not found"
                }
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)       
        context['object_list'] = Top250Movies.objects.filter(rank__isnull=False)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        option = self.request.GET.get('option')
        order = self.request.GET.get('order', 'asc')

        if option == 'rating':
            if order == 'asc':
                queryset = queryset.order_by('-rating')
            elif order == 'desc':
                queryset = queryset.order_by('rating')
        elif option == 'release_date':
            if order == 'asc':
                queryset = queryset.order_by('year')
            elif order == 'desc':
                queryset = queryset.order_by('-year')

        """ if year_order == 'asc':
            queryset = queryset.order_by('year')
        elif year_order == 'desc':
            queryset = queryset.order_by('-year') """
        
        return queryset
        
        if self.request.GET.get('title'):
            queryset = queryset.filter(title=self.request.GET.get('title'))
        return Top250MoviesFilter(self.request.GET, queryset=queryset).qs
  

        

class MovieMostPopular(ListView):
    template_name = 'Movies/movies-most-popular.html'
    context_object_name = 'movies'  
    paginate_by = 15
    is_paginated = True
    
    def get(self, request):
        url = f'https://imdb-api.com/en/API/MostPopularMovies/{api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            movies = data['items']
        else:
            movies = []

        #filter contextmovies from ascending rating 
        context = {
            'movies': movies
        }
        return render(request, self.template_name, context) 
    

def inTheater(request):
    if request.method == "GET":
        url = f"https://imdb-api.com/en/API/InTheaters/{api_key}"
        response = requests.get(url)
        dataset = response.json()
        try:
            context = {
                "movies": dataset["items"],
            }
        except:
            context = {
                "error": "Movie not found"
            }
        return render(request, 'Movies/movie-theater.html', context)
    
def comingSoon(request):
    if request.method == "GET":
        url = f"https://imdb-api.com/en/API/ComingSoon/{api_key}"
        response = requests.get(url)
        dataset = response.json()
        try:
            context = {
                "movies": dataset["items"],
            }
        except:
            context = {
                "error": "Movie not found"
            }
        return render(request, 'Movies/movie-coming-soon.html', context)
    

""" def top250movies(request):
    if request.method == 'GET':
        url = f"https://imdb-api.com/en/API/Top250Movies/{api_key}"
        response = requests.get(url)
        dataset = response.json()
        try:
            context = {
                "movies": Top250Movies.objects.all(),
                }
            
                response_json = dataset["items"]
                # filter with the keys that wants to add to the db
                keys_to_add = ["rank", "title", "year", "image", "crew", ]
                
                # function for delete duplicate rows
                for row in Movie.objects.all().reverse():
                    if Movie.objects.filter(rank=row.rank).count() > 1:
                        row.delete()


            #a bucle for iterate in the json response and add the filter keys
            with transaction.atomic():
                
                for item in response_json:
                    list_dict = []
                    
                    if range(len(list_dict)) == 0:
                        continue
                    for key, values in item.items():
                        if key in keys_to_add:
                            list_dict.append(values)
                    if range(len(list_dict)) == 0:
                        continue
                    print(list_dict)
                    
                    movie = Movie(rank = list_dict[0], title = list_dict[1], year = list_dict[2], image = list_dict[3], crew = list_dict[4])
                    movie.save()
                   
            #add imdbrating to the db 
            with transaction.atomic():
                for movie in Movie.objects.all():
                    for item in dataset['items']:
                        if movie.title == item['title']:
                            movie.rating = item['imDbRating']
                            movie.save()
                            print("db updated")
                            print("========================================")

            
            #cambiar los values de la columna rank de Movie para que se conviertan en tipo Integrer
            with transaction.atomic():
                for movie in Movie.objects.all():
                    movie.rank = int(movie.rank)
                    movie.save()
                    print("db updated")
                    print("========================================")

            #agregar la lista de generos a los objectos de la db
            with transaction.atomic():
                for movie in Top250Movies.objects.all():
                    for item in dataset['items']:
                        if movie.title == item['title']:
                            movie.genre = item['genres']
                            movie.save()
                            print("db updated")
                            print("========================================")
            
        except:
            context = {
                "error": "Server Error"
            }
        
        return render(request, 'movies/movielist.html', context)
    return redirect('home') """