from django.conf.urls import url
from . import views

app_name = 'weatherapp'
urlpatterns = [
    url(r'^select/(?P<id>\w+)', views.RegionWeather ,name='RegionWeather'),
    url(r'^$', views.GetWeather ,name='Create'),
]
