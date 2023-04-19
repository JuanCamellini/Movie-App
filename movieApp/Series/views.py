from django.shortcuts import render, redirect
from django.db import transaction
from django.core.paginator import Paginator
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)

import django_filters 
import requests
import crispy_forms
import json

from api_key import api_key
from .models import Top250Series
from .filters import SeriesFilter, Top250SeriesFilter
from .forms import SeriesFilterForm

# Create your views here.

class SerieListView(ListView):
    model = Top250Series
    template_name = 'Series/serielist.html'
    context_object_name = 'Series'
    paginate_by = 50 
    is_paginated = True

    def get_Series(request):
        if request.method == 'POST':
            Series = request.POST['Series'].lower()
            if " " in Series:
                Series.replace(" ","%20")
                url = f"https://imdb-api.com/en/API/AdvancedSearch/{api_key}/?title={Series}"  
        try:        
            context = {
                "Series": Top250Series.objects.all()
            }
        except:
            context = { 
                "error": "Series not found"
                }
        return render(request, 'Series/serielist.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('title'):
            queryset = queryset.filter(title=self.request.GET.get('title'))
        return Top250SeriesFilter(self.request.GET, queryset=queryset).qs

#function to add the 250 series into the Top250Series 
""" def top250Series(request):
    if request.method == 'GET':
        url = f"https://imdb-api.com/en/API/Top250TVs/{api_key}"
        response = requests.get(url)
        dataset = response.json()
        try:
            # Realizamos el llamado a la API
            response = requests.get('https://imdb-api.com/en/API/Top250TVs/k_t5dpr709')
            response.raise_for_status()  # Comprobamos si hubo algún error en la respuesta
        except requests.exceptions.RequestException as e:
            print(f'Error al hacer la petición a la API: {e}')
            return
        try:
            # Parseamos el contenido de la respuesta a JSON
            data = response.json()
            if 'items' not in data:
                print('La respuesta de la API no contiene items')
                return
        except (json.JSONDecodeError, KeyError) as e:
            print(f'Error al parsear la respuesta de la API: {e}')
            return
        # Guardamos cada item en la base de datos
        for item in data['items']:
            try:
                # Validamos que todos los campos requeridos estén presentes
                required_fields = ['id', 'title', 'year', 'imDbRatingCount', 'rank', 'crew', 'imDbRating', 'image']
                if not all(field in item for field in required_fields):
                    print(f'El item {item["id"]} no tiene todos los campos requeridos')
                    continue
                
                # Creamos un objeto Top250Series y lo guardamos en la base de datos
                top_250_series = Top250Series.objects.create(
                    serie_id=item['id'],
                    title=item['title'],
                    year=item['year'],
                    rank=item['rank'],
                    crew=item['crew'],
                    rating=item['imDbRating'],
                    ratingCount=item['imDbRatingCount'],
                    image=item['image']
                )
                print(f'Se ha guardado en la base de datos la serie {top_250_series.title}')
            except Exception as e:
                print(f'Error al guardar la serie {item["id"]}: {e}')
            
        return render(request, 'Series/serielist.html')
    return redirect('home') """