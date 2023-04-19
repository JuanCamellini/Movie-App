
# Django
from django.contrib import admin

# Models
from .models import Movies, Top250Movies, MoviesLiked

# Top250Movies Admin
class Top250MoviesAdmin(admin.ModelAdmin):
    fields = ["title", "year", "crew", "rank", "image", "rating", "genre"]
    list_display = ("title", "rank", "year", "rating")
    list_filter = ("year", "rank")
    search_fields = ["title", "rank", "crew"]

admin.site.register(Top250Movies, Top250MoviesAdmin)

# Movies Admin
class MoviesAdmin(admin.ModelAdmin):
    fields = ["title", "year", "crew", "image", "rating","genre"]
    list_display = ("title", "year", "rating")
    list_filter = ("year", "genre")
    search_fields = ["title",  "crew", "genre"]

admin.site.register(Movies, MoviesAdmin)

#MoviesLiked Admin
class MoviesLikedAdmin(admin.ModelAdmin):
    fields = ["movie_id", "user_id"]
    list_display = ("movie_id", "user_id")
    list_filter = ("movie_id", "user_id")
    search_fields = ["movie_id", "user_id"]

admin.site.register(MoviesLiked, MoviesLikedAdmin)
