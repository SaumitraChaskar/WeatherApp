from django.shortcuts import render
from .models import City
from .forms import CityForm
import requests
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metricl&APPID=e8e2920b330792de914f097bbded0faa'


    print(request.POST)
    err_mesg = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count() 

            if existing_city_count == 0:
                form.save()
            else:
                err_mesg = 'City already exists'

    form = CityForm()

    cities  = City.objects.all()
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()

    
        Kelvin = r['main']['temp']
        Degree = int(Kelvin)-273
        city_weather = {
            'city':city.name,
            'temperature':Degree,
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)
    
    print(weather_data)

    context = {'weather_data':weather_data,'form':form }

        
    return render(request,'weather/weather.html',context)
