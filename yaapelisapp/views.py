from django.shortcuts import render, redirect,get_object_or_404,get_list_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import requests
import math
import environ
env = environ.Env()
environ.Env.read_env()

# Create your views here.
api_url = "https://api.themoviedb.org/3"
api_key = env.str('API_KEY')

def home_page(request):
    if request.method == 'GET':
        try:
            response = requests.get(f'{api_url}/discover/movie?api_key={api_key}')
            if response.status_code == 200:
                movies = response.json()
                return render(request, "home.html", {
                    "movies": movies["results"]
                })
        except:
            movies =[]
            return render(request, "home.html", {
              "movies": movies,
              "error": "Ha ocurrido un error"
            })
    else:
        try:
            movie_name = request.POST['movie_name']
            response = requests.get(f'{api_url}/search/movie?query={movie_name}&api_key={api_key}')
            movies = response.json()
            return render(request, "home.html", {
              "movies": movies["results"]
            })
        except: 
            movies =[]
            return render(request, "home.html", {
              "movies": movies,
              "error": "No se encontraron resultados"
            })

      


def singup(request):
    if request.method == "GET":
       return render(request, 'account/signup.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
              user = User.objects.create_user(request.POST['username'], f"request.POST['username']@gmail.com", request.POST['password1'])
              user.save()
              return redirect("signin")
            except:
               return render(request, 'account/signup.html',{
                "error": "La cuenta ya existe"
            })
        else:
            return render(request, 'account/signup.html',{
                "error": "Las contraseñas no coinciden"
            })

           

def signin(request):
    if request.method == 'GET':
       return render(request, 'account/signin.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'account/signin.html',{
               "error": "Datos incorrectos."
            })
        else:
           login(request, user)
           return redirect("home")
        
def sign_out(request):
    logout(request)
    return redirect('home')

def movie_detail(request, movie_id):
    response = requests.get(f'{api_url}/movie/{movie_id}?api_key={api_key}&append_to_response=videos,images')
    key=""
    if response.status_code == 200:
        movie = response.json()
        videos = movie["videos"]["results"]
        for video in videos:
          if video["type"] == 'Trailer':
            key = video["key"]
        age = movie["release_date"].split("-")[0]
        average = math.ceil((movie["vote_average"] * 10))
        return render(request, "details.html",{
          "movie": movie,
          "key": key,
          "age": age,
          "average" : average
       })
    
