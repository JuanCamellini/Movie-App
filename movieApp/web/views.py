# Django
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError

#Utilities
from users.forms import UserRegisterForm
from Movies.models import Movies, Top250Movies, MoviesLiked
from Series.models import Series, Top250Series, SeriesLiked

from api_key import api_key

import json 
import urllib.request
import requests
# Create your views here.

""" def index(request):
    if request.method == 'POST':
        movie = request.POST['movie']
        url = f"https://imdb-api.com/en/API/SearchMovie/{api_key}/{movie}"
        response = requests.get(url)
        dataset = response.json()
        try:
            context = {
                ### 
                "id": dataset['results'][0]['id'],
                "image": dataset['results'][0]['image'],
                "title": dataset['results'][0]['title']
            }
        except:
            context = {
                "error": "Movie not found"
            }


        return render(request, 'webApp/index.html', context)
    return render(request, 'webApp/index.html') """

def index(request):
    if request.method == 'POST':
        if 'movie' in request.POST:
            movie = request.POST['movie'].lower()
            if " " in movie:
                movie.replace(" ","%20")
            url = f"https://imdb-api.com/en/API/AdvancedSearch/{api_key}/{movie}"
            response = requests.get(url)
            dataset = response.json()
            print(dataset)
            
            try:
                context = {
                    ### 
                    "id": dataset['results'][0]['id'],
                    "image": dataset['results'][0]['image'],
                    "title": dataset['results'][0]['title'],
                    "duration": dataset['results'][0]['runtimeStr'],
                    "genres": dataset['results'][0]['genres'],
                    "rating": dataset['results'][0]['imDbRating'],
                    "ratingvotes": dataset['result'][0]['imDbRatingVotes'],
                    "plot": dataset['results'][0]['plot'],
                    "stars": dataset['results'][0]['stars'],
                    "director":dataset['results'][0]['starList'][0]['name'],
                }
            except:
                context = {
                    "error": "Movie not found"
                }
            return render(request, 'webApp/moviesingle.html', context)

        
                
    else: 
        form = UserRegisterForm()

        
    return render(request, 'webApp/index.html', {'form': form})

#Functions for the results view
def movie_or_serie_in_database(movie_title):
    """ Check if movie or serie is in the database """
    if Movies.objects.filter(title__icontains=movie_title).exists():
        return True
    elif Series.objects.filter(title__icontains=movie_title).exists():
        return False
    else:
        return None

def clean_movie_title(title):
    """Clean and validate the movie title."""
    return title.lower().replace(" ", "%20")

def fetch_movie_data(movie_title):
    """Fetch data about a movie from the IMDb API."""
    url = f"https://imdb-api.com/API/AdvancedSearch/{api_key}/?title={movie_title}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

#create a fucntion that fetch_movie_trailer
def fetch_movie_trailer(movie_id):
    """Fetch additional details about a movie from the IMDb API."""
    url = f"https://imdb-api.com/en/API/Trailer/{api_key}/{movie_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_movie_details(movie_id):
    """Fetch additional details about a movie from the IMDb API."""
    url = f"https://imdb-api.com/en/API/Title/{api_key}/{movie_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def validate_movie_data(data):
    """Validate the data returned from the IMDb API."""
    for key, value in data.items():
        try:
            Movies._meta.get_field(key).run_validators(value)
        except ValidationError:
            return False
    return True

def movie_or_serie(contentRating):
    """Validate the data returned from the IMDb API."""
    if not "TV" in contentRating :
        return True
    else:
        return False

# crear funcion q si el titulo se encuentra en la db q no realice el pedido api 
def results(request):
    if request.method == 'POST':
        movie_title = clean_movie_title(request.POST['movie'])
        # if the movie or serie is in the database take the data from there
        if movie_or_serie_in_database(movie_title):
            movie = Movies.objects.get(title__icontains=movie_title)
            return render(request, 'Movies/movies-detail.html', {'movie':movie})
        elif movie_or_serie_in_database(movie_title) == False:
            serie = Series.objects.get(title=movie_title)
            return render(request, 'Series/series-detail.html', {'serie':serie} )
        else:
            try:
                data = fetch_movie_data(movie_title)['results'][0]
            except (requests.RequestException, IndexError):
                return render(request, 'webApp/404.html')
            context = {
                "movie_id": data['id'],
                "image": data['image'],
                "title": data['title'],
                "year": data['description'].replace("(", "").replace(")",""),
                "duration": data['runtimeStr'],
                "genre": data['genres'],
                "rating": data['imDbRating'],
                "plot": data['plot'],
                "crew": data['stars'],
                "director": data['starList'][0]['name'],
                "contentRating": data["contentRating"],
            }
            try:
                #add keys to the context but not in the table
                details = fetch_movie_details(context['movie_id'])
                context["releaseDate"] = details["releaseDate"]
                context["awards"] = details["awards"]
                context["writers"] = details["writers"]
                context["keywordList"] = details["keywordList"]

                details = fetch_movie_trailer(context['movie_id'])
                context["trailer"] = details["link"]
            except requests.RequestException:
                pass

            if movie_or_serie(context["contentRating"]):
                #for movies
                context["rating"] = float(context["rating"])                 
                keys_to_add = ["movie_id", "image", "title", "year", "duration", "genre", "rating", "plot", "crew", "director"]
                context_db = {key: value for key, value in context.items() if key in keys_to_add}
                print(context_db)
                if validate_movie_data(context_db):
                    movie_instance, created = Movies.objects.get_or_create(
                        title=context['title'],  
                        movie_id=context['movie_id'],
                        image=context['image'],
                        year=context['year'],
                        duration=context['duration'],
                        genre=context['genre'],
                        rating=context['rating'],
                        plot=context['plot'],
                        crew=context['crew'],
                        director=context['director']
                            )
                    if created:
                        movie_instance.save()
                    print("=========================================")
                    print(movie_instance)
                    return render(request, 'webapp/moviesingle.html', context)
            else:
                #for series
                context["rating"] = float(context["rating"])                 
                keys_to_add = ["movie_id", "image", "title", "year", "duration", "genre", "rating", "plot", "crew", "director"]
                context_db = {key: value for key, value in context.items() if key in keys_to_add}
                print(context_db)
                if validate_movie_data(context_db):
                    serie_instance, created = Series.objects.get_or_create(
                        title=context['title'],  
                        series_id=context['movie_id'],
                        image=context['image'],
                        year=context['year'],
                        duration=context['duration'],
                        genre=context['genre'],
                        rating=context['rating'],
                        plot=context['plot'],
                        crew=context['crew'],
                        director=context['director']
                            )
                    if created:
                        serie_instance.save()
                    print("=========================================")
                    print(serie_instance)
                    return render(request, 'webapp/seriessingle.html', context)
                #if the data is not validated return 404
                else:
                    return render(request, 'webapp/404.html')
    else:
        return redirect('home')
    
#old view results
""" def results(request):
    if request.method == 'POST':
        movie = request.POST['movie'].lower()
        if " " in movie:
            movie.replace(" ","%20")
        url = f"https://imdb-api.com/API/AdvancedSearch/{api_key}/?title={movie}"
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
                "api_key": api_key,
                
            }
            url = f"https://imdb-api.com/en/API/Trailer/{api_key}/{context['id']}"
            response = requests.get(url)
            dataset = response.json()
            context["trailer"] = dataset["link"]
            url = f"https://imdb-api.com/en/API/Title/{api_key}/{context['id']}"
            response = requests.get(url)
            dataset = response.json()
            context["releaseDate"] = dataset["releaseDate"]
            context["awards"] = dataset["awards"]
            context["writers"] = dataset["writers"]
            context["keywordList"] = dataset["keywordList"]
            #create context for images 
            print(context['title'])
            
            for key, value in context.items():
                try:
                    # If a field fails validation, an exception is thrown.
                    Movies._meta.get_field(key).run_validators(value)
                except ValidationError:
                    #  If an exception is thrown, it returns an error response to the user 
                    return "error"

            movie_instance, created = Movies.objects.get_or_create(id=context['id'], defaults=context)

            if not created:
                for key, value in context.items():
                    setattr(movie_instance, key, value)
                movie_instance.save()

            # Devolver una respuesta al usuario
            return HttpResponse("Datos guardados correctamente")

            except (KeyError, IndexError):
            # Si se produce una excepción, devuelve una respuesta de error al usuario
            return HttpResponseBadRequest("No se pudo obtener los datos de la película")

        except:
            context = {
                "error": "Movie not found"
                }
        

        return render(request, 'webApp/moviesingle.html', context)
    return redirect('home')"""


def error404(request):
    return render(request, 'webApp/404.html')