from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import UserRegisterForm, UserUpdateForm
from Movies.models import MoviesLiked, Movies

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
    #context = {'movies':movies}
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

@login_required
def favoritemovies(request):
    #add comments for every line of code

    #get the user
    user = request.user

    #get the movies liked by the user
    movie_id = user.moviesliked_set.values_list('movie_id', flat=True)
    
    #get the movies and filter 
    movies = Movies.objects.filter(id__in = movie_id)

    context = {'movies':movies}
    return render(request, 'users/favoritemovies.html', context)    

@login_required
def favoriteseries(request):
    #add comments for every line of code

    #get the user
    user = request.user

    #get the series liked by the user
    serie_id = user.moviesliked_set.values_list('serie_id', flat=True)
    
    #get the series and filter 
    series = Movies.objects.filter(id__in = serie_id)

    context = {'series':series}
    return render(request, 'users/favoriteseries.html', context)    
@login_required
def userrate(request):
    return render(request, "users/userrate.html")

@login_required
def userfavoritegrid(request):
    return render( request, "users/userfavoritegrid.html")