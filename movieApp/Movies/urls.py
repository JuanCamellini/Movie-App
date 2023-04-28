from django.contrib import admin
from django.urls import path, include
from web.views import results

from .views import (
    MovieListView,
    MovieMostPopular,
    inTheater,
    comingSoon
    )

urlpatterns = [
    path('top-250/', MovieListView.as_view(), name="topmovies"),
    path('most-popular/', MovieMostPopular.as_view(), name="mostpopularmovies"),
    path('detail/<int:pk>', results, name="detailmovie" ),
    path('in-theaters/', inTheater, name="intheaters" ),
    path('cooming-soon/', comingSoon, name="comingsoon"),
]