from django.contrib import admin
from django.urls import path, include

from .views import ( 
    SerieListView,
    SerieMostPopular    
    )

urlpatterns = [
    #path('top250/', top250Series, name="top250series"),
    path('top-250/', SerieListView.as_view(), name="topseries"),
    path('most-popular/', SerieMostPopular.as_view(), name="mostpopularseries" )
]