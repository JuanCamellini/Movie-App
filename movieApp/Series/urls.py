from django.contrib import admin
from django.urls import path, include

from .views import ( 
    SerieListView
    )

urlpatterns = [
    #path('top250/', top250Series, name="top250series"),
    path('top-250-series/', SerieListView.as_view(), name="topseries")
]