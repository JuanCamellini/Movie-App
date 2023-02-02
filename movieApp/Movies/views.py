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
            response_json = dataset["items"]
            #a counter to add the value from the key
            counter = 0
            #a filter with the keys that wants to add to the context
            keys_to_add = ["rank", "title", "year", "image", "crew"]
            #bucle for iterate in the dictionary and updates the context
            """ for item in response_json:
                if item == item:
                    counter += 1
                for key, value in item.items():
                    if key in keys_to_add:  
                        with transaction.atomic():
                            movie = Movie(**value)
                            movie.save() """
            
            """ for item in response_json:        
                for key, value in item.items():
                    counter+=1
                    if counter >= 50:
                        break
                    if key in keys_to_add:
                        
                        with transaction.atomic():
                            movie = Movie(key = value)
                            movie.save()
                            print("db succesful")  """
        

        except:
            context = {
                "error": "Server Error"
            }
        with transaction.atomic():
            
            for item in response_json:
                list_dict = []
                
                if range(len(list_dict)) == 0:
                    continue
                for key, values in item.items():
                    counter += 1
                    if counter >= 54:
                        break
                    if key in keys_to_add:
                        list_dict.append(values)
                
                movie = Movie(rank = list_dict[0], title = list_dict[1], year = list_dict[2], image = list_dict[3], crew = list_dict[4])
                movie.save()
                print("db succesful")
                print(list_dict)

        return render(request, 'webApp/movielist.html', context)
    return redirect('home')