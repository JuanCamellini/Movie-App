import django_filters

from .models import Movie

class MovieFilter(django_filters.FilterSet):

    class Meta:
        model = Movie
        fields = {
            'title':['icontains'],
            'year':['lt', 'gt'],
            'rank':['lt', 'gt'],
            }
