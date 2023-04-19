# Register your models here.
from django.contrib import admin

# Models
from .models import Series, Top250Series, SeriesLiked

# Top250Movies Admin
class Top250SeriesAdmin(admin.ModelAdmin):
    fields = ["title", "year", "crew", "rank", "image", "rating", "ratingCount"]
    list_display = ("title", "rank", "year", "rating")
    list_filter = ("year", "rank")
    search_fields = ["title", "rank", "crew"]

    def get_queryset(self, request):
        queryset = super(Top250SeriesAdmin, self).get_queryset(request)
        queryset = queryset.order_by('rank')
        return queryset
    

admin.site.register(Top250Series, Top250SeriesAdmin)

# Movies Admin
class SeriesAdmin(admin.ModelAdmin):
    fields = ["title", "year", "crew", "image", "rating"]
    list_display = ("title", "year", "rating")
    list_filter = ("year",)
    search_fields = ["title",  "crew"]

admin.site.register(Series, SeriesAdmin)

# SeriesLiked Admin
class SeriesLikedAdmin(admin.ModelAdmin):
    fields = ["movie_id", "user_id"]
    list_display = ("movie_id", "user_id")
    list_filter = ("movie_id", "user_id")
    search_fields = ["movie_id", "user_id"]

admin.site.register(SeriesLiked, SeriesLikedAdmin)
