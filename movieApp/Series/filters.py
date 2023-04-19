import django_filters

from .models import Series, Top250Series

class SeriesFilter(django_filters.FilterSet):

    class Meta:
        model = Series
        fields = {
            'title':['icontains'],
            'year':['lt', 'gt'],
            }

class Top250SeriesFilter(django_filters.FilterSet):
    
        class Meta:
            model = Top250Series
            fields = {
                'title':['icontains'],
                'year':['lt', 'gt'],
                'rank':['lt', 'gt'],
                }
            