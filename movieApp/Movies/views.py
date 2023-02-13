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

from api_key import api_key
from .models import Movie
from .filters import MovieFilter

# Create your views here.

class MovieListView(ListView):
    model = Movie
    template_name = 'Movies/movielist.html'
    context_object_name = 'movies'
    paginate_by = 50    

    def get_movie(request):
        if request.method == 'POST':
            movie = request.POST['movie'].lower()
            if " " in movie:
                movie.replace(" ","%20")
                url = f"https://imdb-api.com/en/API/AdvancedSearch/{api_key}/?title={movie}"
            response = requests.get(url)
            dataset = response.json()

        

        """ movie_list = Movie.objects.all()
        # Set up Paginator
        p = Paginator(Movie.objects.all(), 50)
        page = request.GET.get('page')
        movies = p.get_page(page) """
        
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
        except:
            context = { 
                "error": "Movie not found"
                }
        return render(request, 'Movies/movielist.html', context)

    """ def sort_by(request):
        #hacer un sort_by del rating de las peliculas en forma ascendente y descendiente, y año ascendente
        movies_list_descending = Movie.objects.all().order_by('-rating')
        movies_list_ascending = Movie.objects.all().order_by('rating')
        movies_list_year_ascending = Movie.objects.all().order_by('year')
        movies_list_year_descending = Movie.objects.all().order_by('-year')

        context = {
            "movies_rating_descending": movies_list_descending,
            "movies_rating_ascending": movies_list_ascending,
            "movies_year_ascending": movies_list_year_ascending,
            "movies_year_descending": movies_list_year_descending,
        }

        return render(request, 'Movies/movielist.html', context) """

    def get_queryset(self):
        movies = Movie.objects.all().filter(rank__isnull=False)
        #listing_movies = MovieFilter(queryset=movies)
        return movies
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    


def top250movies(request):
    if request.method == 'GET':
        url = f"https://imdb-api.com/en/API/Top250Movies/{api_key}"
        response = requests.get(url)
        dataset = response.json()
        try:
            context = {
                "movies": Movie.objects.all(),
                }
            """
                response_json = dataset["items"]
                # filter with the keys that wants to add to the db
                keys_to_add = ["rank", "title", "year", "image", "crew"]
                
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
                    """
            """ #add imdbrating to the db 
            with transaction.atomic():
                for movie in Movie.objects.all():
                    for item in dataset['items']:
                        if movie.title == item['title']:
                            movie.rating = item['imDbRating']
                            movie.save()
                            print("db updated")
                            print("========================================")

             """
            #cambiar los values de la columna rank de Movie para que se conviertan en tipo Integrer
            with transaction.atomic():
                for movie in Movie.objects.all():
                    movie.rank = int(movie.rank)
                    movie.save()
                    print("db updated")
                    print("========================================")

            """ #agregar la lista de generos a los objectos de la db
            with transaction.atomic():
                for movie in Movie.objects.all():
                    for item in dataset['items']:
                        if movie.title == item['title']:
                            movie.genre = item['genres']
                            movie.save()
                            print("db updated")
                            print("========================================") """
            
        except:
            context = {
                "error": "Server Error"
            }
        
            

        return render(request, 'movies/movielist.html', context)
    return redirect('home')