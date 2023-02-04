from django.contrib import admin
from .models import Movie
# Register your models here.



class MovieAdmin(admin.ModelAdmin):
    fields = ["title", "year", "crew", "rank", "image"]
    list_display = ("title", "rank", "year")
    list_filter = ("year", "rank")
    search_fields = ["title", "rank", "crew"]

admin.site.register(Movie, MovieAdmin)