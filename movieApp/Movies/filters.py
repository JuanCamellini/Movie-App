import django_filters

from .models import Movies, Top250Movies

class MoviesFilter(django_filters.FilterSet):

    class Meta:
        model = Movies
        fields = {
            'title':['icontains'],
            'year':['lt', 'gt'],
            }

class Top250MoviesFilter(django_filters.FilterSet):
    
        class Meta:
            model = Top250Movies
            fields = {
                'title':['icontains'],
                'year':['lt', 'gt'],
                'rank':['lt', 'gt'],
                'genre':[]
                }
            