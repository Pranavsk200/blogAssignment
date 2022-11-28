from django.shortcuts import render,redirect
from .models import WeatherRepost
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login,logout
import json
import urllib.request

def index(request):
    # if request.method == 'POST' :
    #     city = request.POST['city']
    #     if WeatherRepost.objects.filter(city__icontains = city).exists():
    #         weather = WeatherRepost.objects.filter(city__icontains = city)
    #     else:
    #         weather = "city not found"
    #     context = {
    #         'weather':weather
    #     }
    #     return render(request, 'index.html', context)
    # return render(request, 'index.html')
    if request.user.is_authenticated:
        try:
            if request.method == 'POST':
                city = request.POST['city']
                source = urllib.request.urlopen(
                    'http://api.openweathermap.org/data/2.5/weather?q =' 
                            + city + '&appid = your_api_key_here').read()
                list_of_data = json.loads(source)
                data = {
                    "country_code": str(list_of_data['sys']['country']),
                    "coordinate": str(list_of_data['coord']['lon']) + ' '
                                + str(list_of_data['coord']['lat']),
                    "temp": str(list_of_data['main']['temp']) + 'k',
                    "pressure": str(list_of_data['main']['pressure']),
                    "humidity": str(list_of_data['main']['humidity']),
                }
                print(data)
            else:
                data ={}
            return render(request, "index.html", data)
        except:
            if request.method == 'POST' :
                city = request.POST['city']
                if WeatherRepost.objects.filter(city__icontains = city).exists():
                    weather = WeatherRepost.objects.filter(city__icontains = city)[0]
                    context = {
                    "code": str("IN"),
                    "coordinate": " ",
                    "temp": weather.temp,
                    "pressure": weather.pressure,
                    "humidity": weather.humidity,
                    }
                else:
                    context={
                        "weather": "city not found"
                    }
                    weather = "city not found"
                
                return render(request, 'index.html', context)
            return render(request, 'index.html')
    else:
        return redirect("login")            


def searchCity(request,name=None):
    names = []
    cityName = WeatherRepost.objects.all()
    for name in cityName:
        names.append(str(name.city))
    context={
        "data":names
    }
    return JsonResponse(context)

def login(request):
    if request.method=='POST':
        name = request.POST['username']
        password = request.POST['pass']
        user=authenticate(request, username=name, password=password)
        if user is not None:
            dj_login(request, user)
            current_user=request.user
            return redirect("home")
        else:
            #messages.success(request, "username or password is incorrect") 
            return redirect("login")   
    else:    
        return render(request,"login.html")

def signin(request):
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['pass']
        repassword = request.POST['repass']
        if password==repassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,"user name already exists,please resistor with another username") 
                return redirect("signin")   
            else:    
                user =User.objects.create_user(username=username, password=password)
                user.save()
                print('user created')
                return redirect("login")
        else:
            messages.info(request, "conform passowerd and password are not matching")
    else:
        return render(request, "signin.html") 

def logoutUser(request):
    if request.user.is_authenticated: 
        logout(request)
        return redirect("login") 
    else:
        return redirect("login")
    