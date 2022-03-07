from .forms import DocumentForm, CityForm, CoordForm
from .models import Cities
from rest_framework import generics
from django.shortcuts import render
from cities_light.models import City
from django.shortcuts import  get_object_or_404
from .tasks import check_weather
from datetime import datetime
import json
from django.db import transaction
import pandas as pd


def getdb(r, city):
    id = city.id
    now = datetime.now()
    lat = r['coord']['lat']
    lon = r['coord']['lon']
    weather_id = r['weather'][0]['id']
    weather_main = r['weather'][0]['main']
    weather_description = r['weather'][0]['description']
    weather_icon = 'http://openweathermap.org/img/wn/' + r['weather'][0]['icon'] + '@2x.png'
    temp = r['main']['temp']
    feels_like = r['main']['feels_like']
    temp_min = r['main']['temp_min']
    temp_max = r['main']['temp_max']
    humidity = r['main']['humidity']
    visibility = r['visibility']
    wind_speed = r['wind']['speed']
    wind_deg = r['wind']['deg']

    wheather_dict = {
            'weather_main': weather_main,
            'weather_description': weather_description,
            'feels_like': feels_like,
            'weather_icon': weather_icon,
            'temp': temp,
            'temp_min': temp_min,
            'temp_max': temp_max,
            'humidity': humidity,
            'visibility': visibility,
            'wind_speed': wind_speed,
            'wind_deg': wind_deg,
            'id': id,
            'now': now,
            'city': city,
            'lat': lat,
            'lon': lon,
                            }
    return wheather_dict


def get_reg_db(r, city, set_wheather):

    set_wheather.append(city)
    set_wheather.append(r['weather'][0]['main'])
    set_wheather.append(datetime.now())
    set_wheather.append('http://openweathermap.org/img/wn/' + r['weather'][0]['icon'] + '@2x.png')
    set_wheather.append(r['weather'][0]['description'])
    set_wheather.append(r['main']['temp'])
    set_wheather.append(r['main']['feels_like'])
    set_wheather.append(r['main']['temp_min'])
    set_wheather.append(r['main']['temp_max'])
    set_wheather.append(r['main']['humidity'])
    set_wheather.append(r['visibility'])
    set_wheather.append(r['wind']['speed'])
    set_wheather.append(r['wind']['deg'])

    return set_wheather

@transaction.atomic
def RegionWeather(request, id):
    df_wheather = pd.DataFrame(columns=['city', 'weather_main', 'now', 'weather_icon', 'weather_description', 'temp', 'feels_like', 'temp_min', 'temp_max', 'humidity', 'visibility', 'wind_speed', 'wind_deg'])

    check_db = City.objects.filter(id=id)
    region_id = check_db[0].region_id
    region_db = City.objects.filter(region_id=region_id)

    for city in region_db:
            set_wheather = []
            lat = city.latitude
            lon = city.longitude
            id = city.id
            now = datetime.now()
            check_db = Cities.objects.filter(city=id)
            if check_db:
                date = check_db[0].date
                if (now.timestamp() - date.timestamp()) < 3600*24:
                    r = check_db[0].weather
                    r = r.replace("'", '"')
                    r = json.loads(r)
                    set_wheather = get_reg_db(r, city, set_wheather)
                    check_db.delete()
                    df_wheather.loc[len(df_wheather)] = set_wheather
            else:
                r = check_weather(lat, lon)
                if r != 'ERR':
                    weather_cities = Cities(
                                    city=city,
                                    weather=r,
                                )
                    weather_cities.save()
                    set_wheather = get_reg_db(r, city, set_wheather)
                    df_wheather.loc[len(df_wheather)] = set_wheather

    df_wheather = df_wheather.sort_values(by='temp', ascending=False)
    mas = []
    len_df = len(df_wheather.index)
    for l in range(len_df):
        mas.append(df_wheather.iloc[l].values)

    return render(request, 'weather_for_region.html', {
        'mas' : mas,
    })




@transaction.atomic
def GetWeather(request):

    if request.method == 'POST':
        city_form = DocumentForm(request.POST)
        if city_form.is_valid():
            city=city_form.cleaned_data['city']
            lat = city.latitude
            lon = city.longitude
            id = city.id
            now = datetime.now()
            check_db = Cities.objects.filter(city_id=id)
            if check_db:
                date = check_db[0].date
                if (now.timestamp() - date.timestamp()) < 3600*24:
                    r = check_db[0].weather
                    r = r.replace("'", '"')
                    r = json.loads(r)
                    wheather_dict = getdb(r, city)
                    return render(request, 'weather.html', wheather_dict)
                check_db.delete()
            r = check_weather(lat, lon)
            if r != 'ERR':
                    weather_cities = Cities(
                                    city=city,
                                    weather=r,
                                )
                    weather_cities.save()
                    wheather_dict = getdb(r, city)
                    return render(request, 'weather.html', wheather_dict)

            else:
                    city_form = DocumentForm(request.POST)
                    error = 'Failed to connect to the server at the moment. Try again later.'
                    return render(request, 'main.html', {
                                'city_form': city_form,
                                'error': error,
                            })

        else:
            coord_form = CoordForm(request.POST)
            if coord_form.is_valid():
                now = datetime.now()
                lat=coord_form.cleaned_data['Latitude']
                lon=coord_form.cleaned_data['Longitude']
                check_db = Cities.objects.filter(Latitude=lat, Longitude=lon )

                if check_db:
                    date = check_db[0].date
                    if (now.timestamp() - date.timestamp()) < 3600*24:
                        r = check_db[0].weather
                        r = r.replace("'", '"')
                        r = json.loads(r)
                        city = check_db[0].city
                        wheather_dict = getdb(r, city)
                        return render(request, 'weather.html', wheather_dict)
                    check_db.delete()
                else:
                    r = check_weather(lat, lon)
                    if r != 'ERR':
                        check_db = City.objects.filter(latitude=lat, longitude=lon )
                        if check_db:
                            city=check_db
                        else:
                            geoname_id = r['id']
                            check_db = City.objects.get(geoname_id=292239)
                            if check_db != []:
                                city=check_db[0]

                        weather_cities = Cities(
                                        city=city,
                                        weather=r,
                                        Latitude=lat, Longitude=lon
                                    )
                        weather_cities.save()
                        wheather_dict = getdb(r, city)
                        return render(request, 'weather.html', wheather_dict)

                    else:
                        coord_form = CoordForm(request.POST)
                        error = 'Failed to connect to the server at the moment. Try again later.'
                        return render(request, 'main.html', {
                                    'city_form': city_form,
                                    'coord_form': coord_form,
                                    'error': error,
                                })


    city_form = DocumentForm(request.POST)
    coord_form = CoordForm(request.POST)

    return render(request, 'main.html', {
                'city_form': city_form,
                'coord_form': coord_form,

            })




def MainHtml(request):

    return render(request, 'main.html')
