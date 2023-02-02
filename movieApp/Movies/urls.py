from django.contrib import admin
from django.urls import path, include

from .views import top250movies

urlpatterns = [
    path('top250/', top250movies, name="top250movies")
]