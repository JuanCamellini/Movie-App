from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction

from .forms import UserRegisterForm, UserUpdateForm
from Movies.models import Movie

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
            url = f"https://imdb-api.com/en/API/SearchMovie/{api_key}/{movie}"
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

        elif 'username' in request.POST:
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, "Account created for " + username)
                return redirect('login')
        return render(request, "users/userprofile.html")
                
    else: 
        form = UserRegisterForm()

        
    return render(request, 'webApp/index.html', {'form': form})




def results(request):
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
                "api_key": api_key,
                
            }
            print(context)
            url = f"https://imdb-api.com/en/API/Trailer/{api_key}/{context['id']}"
            response = requests.get(url)
            dataset = response.json()
            context["trailer"] = dataset["link"]

        except:
            context = {
                "error": "Movie not found"
                }

        with transaction.atomic():
            if not Movie.objects.filter(title=context['title']).exists():
                year = context['year'].replace("(", "").replace(")","")
                Movie.objects.create(
                    title=context['title'],
                    year=year,
                    #genre=context['genres'],
                    rating=context['rating'],
                    crew=context['stars'],
                    image=context['image'],
                )
                print("db succesfuly")
                print("=====================================")
                print(context['title'])

        return render(request, 'webApp/moviesingle.html', context)
    return redirect('home')



