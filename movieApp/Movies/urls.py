from django.contrib import admin
from django.urls import path, include

from .views import (
    top250movies, 
    MovieListView
    )

urlpatterns = [
    path('top250/', top250movies, name="top250movies"),
    path('top/', MovieListView.as_view(), name="topmovies")
]