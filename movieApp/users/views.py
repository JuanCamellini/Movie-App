from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.core.cache import cache

from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm
from Movies.models import MoviesLiked, Movies
from Series.models import SeriesLiked, Series

# Create your views here.
""" @login_required(login_url='login')
@allowed_users(allowed_roles=['customer']) """

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, "Your account has been created!"
                )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'webapp/register.html', {'form_register': form})

def login(request):
    pass

@login_required
def profile(request):
    if request.method == 'POST':
        update_form = UserUpdateForm(request.POST, instance=request.user )
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Your account has been updated")
            return redirect('profile')
    else:
        update_form = UserUpdateForm(instance=request.user)

    context = {'update_form':update_form}
    
    return render(request, 'users/profile.html', context)


        
class FavoriteSeries(LoginRequiredMixin, ListView):
    model = SeriesLiked
    template_name = 'users/favoriteseries.html'
    context_object_name = 'series'
    paginate_by = 5 
    is_paginated = True

    def get_user_favorites(self):
        user = self.request.user
        cache_key = f'series_liked_by_user_{user.id}'
        series = cache.get(cache_key)
        if not series:
            serie_id = user.seriesliked_set.values_list('serie_id', flat=True)
            series = Series.objects.prefetch_related('serieimage_set').filter(id__in=serie_id).values(
                'year', 'title', 'image', 'crew', 'plot', 'director', 'duration', 'rating')
            cache.set(cache_key, series, timeout=60*60) # cache the result for 1 hour
        return series

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['series'] = self.get_user_favorites()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

class FavoriteMovies(LoginRequiredMixin, ListView):
    model = MoviesLiked
    template_name = 'users/favoritemovies.html'
    context_object_name = 'movies'
    paginate_by = 5 
    is_paginated = True

    def get_user_favorites(self):
        user = self.request.user
        cache_key = f'movies_liked_by_user_{user.id}'
        movies = cache.get(cache_key)
        if not movies:
            movie_id = user.moviesliked_set.values_list('movie_id', flat=True)
            movies = Movies.objects.prefetch_related('movieimage_set').filter(id__in=movie_id).values(
                'year', 'title', 'image', 'crew', 'plot', 'director', 'duration', 'rating')
            cache.set(cache_key, movies, timeout=60*60) # cache the result for 1 hour
        return movies

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['series'] = self.get_user_favorites()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

@login_required
def favoriteMovies(request):
    #add comments for every line of code

    #get the user
    user = request.user

    #get the movies liked by the user
    movie_id = user.moviesliked_set.values_list('movie_id', flat=True)
    
    #get the movies and filter 
    movies = Movies.objects.filter(id__in = movie_id)

    context = {'movies':movies}
    return render(request, 'users/favoritemovies.html', context)    


""" @login_required
def favoriteSeries(request):
    #add comments for every line of code

    #get the user
    user = request.user

    #get the series liked by the user
    serie_id = user.seriesliked_set.values_list('serie_id', flat=True)
    
    #get the series and filter 
    series = Series.objects.filter(id__in = serie_id)

    context = {'series':series}
    return render(request, 'users/favoriteseries.html', context)   """  
@login_required
def userRate(request):
    return render(request, "users/userrate.html")

@login_required
def userFavoriteGrid(request):
    return render( request, "users/userfavoritegrid.html")