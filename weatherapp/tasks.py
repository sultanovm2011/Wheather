from celery import task
import requests



@task
def check_weather(lat, lon):
    token = "6c01bbd693a8200df2a1c593f2f25ce2"
    url = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lon) + "&appid=" + token

    try:
        r = requests.get(url, timeout = 15).json()
    except:
        r = 'ERR'

    return r
