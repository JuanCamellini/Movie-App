from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

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
    return render(request, 'webApp/index.html')

def results(request):
    if request.method == 'POST':
        movie = request.POST['movie'].lower()
        if " " in movie:
            movie.replace(" ","%20")
        url = f"https://imdb-api.com/en/API/AdvancedSearch/{api_key}/?title={movie}"
        response = requests.get(url)
        dataset = response.json()
        print(dataset)
        print("##################")
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

            print(context)
        return render(request, 'webApp/moviesingle.html', context)
    return redirect('home')

""" @login_required(login_url='login')
@allowed_users(allowed_roles=['customer']) """
def profile(request):
    #movies = request.user.customer.movies_set.all()
    #context = {'movies':movies}
    if request.method == 'POST':
        update_form = UserUpdateForm(request.POST, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Your account has been updated")
            return redirect('profile')
    else:
        update_form = UserUpdateForm(instance=request.user)

    context = {'update_form':update_form}
    
    return render(request, 'webApp/userprofile.html', context)