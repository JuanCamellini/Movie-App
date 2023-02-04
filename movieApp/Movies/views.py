from django.shortcuts import render, redirect
from django.db import transaction
import requests

from api_key import api_key
from .models import Movie

# Create your views here.
def top250movies(request):
    if request.method == 'GET':
        url = f"https://imdb-api.com/en/API/Top250Movies/{api_key}"
        response = requests.get(url)
        dataset = response.json()
        try:
            context = {

            }
            """
                response_json = dataset["items"]
                # filter with the keys that wants to add to the db
                keys_to_add = ["rank", "title", "year", "image", "crew"]
                
                # function for delete duplicate rows
                for row in Movie.objects.all().reverse():
                    if Movie.objects.filter(rank=row.rank).count() > 1:
                        row.delete()


            #a bucle for iterate in the json response and add the filter keys
            with transaction.atomic():
                
                for item in response_json:
                    list_dict = []
                    
                    if range(len(list_dict)) == 0:
                        continue
                    for key, values in item.items():
                        if key in keys_to_add:
                            list_dict.append(values)
                    if range(len(list_dict)) == 0:
                        continue
                    print(list_dict)
                    
                    movie = Movie(rank = list_dict[0], title = list_dict[1], year = list_dict[2], image = list_dict[3], crew = list_dict[4])
                    movie.save()
                    """

        except:
            context = {
                "error": "Server Error"
            }
        
            

        return render(request, 'movies/movielist.html', context)
    return redirect('home')