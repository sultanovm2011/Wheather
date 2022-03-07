id = 1
now = 2
lat = 3
lon = 4
weather_id = 5
weather_main = 6
weather_description = 7
weather_icon = 8
temp = 9
feels_like = 10
temp_min = 11
temp_max = 12
humidity = 13
visibility = 14
wind_speed = 15
wind_deg = 16

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
        'lat': lat,
        'lon': lon,

                        }
for d in wheather_dict.values():
    print(d)
