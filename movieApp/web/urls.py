from django.contrib import admin
from django.urls import path

from .views import index, results, profile, favoritelist

urlpatterns = [
    path('', index, name="home"),
    path('results/', results, name="results"),
    path('profile/', profile, name="profile"),
    path('favoritelist/', favoritelist, name="favoritelist")

    
]