from django.contrib import admin
from django.urls import path, include

from .views import (
    MovieListView
    )

urlpatterns = [
    path('top-250-movies/', MovieListView.as_view(), name="topmovies")
]