from django.contrib import admin
from django.urls import path, include

from .views import (
    profile,
    favoritelist
    )

urlpatterns = [
    path('profile/', profile, name="profile"),
    path('favoritelist/', favoritelist, name="favoritelist"),
]