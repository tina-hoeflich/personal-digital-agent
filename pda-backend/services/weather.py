import requests
import math

APIKEY = "24e63d1ccffcdbdfd4fa28f7f3c3d861"
base_url = "https://api.openweathermap.org/data/2.5"

data_cache = {'cod': '200', 'message': 0, 'cnt': 8, 'list': [{'dt': 1680598800, 'main': {'temp': 3.95, 'feels_like': 0.11, 'temp_min': 3.38, 'temp_max': 3.95, 'pressure': 1017, 'sea_level': 1017, 'grnd_level': 929, 'humidity': 55, 'temp_kf': 0.57}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'clouds': {'all': 46}, 'wind': {'speed': 4.82, 'deg': 
68, 'gust': 6.84}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2023-04-04 09:00:00'}, {'dt': 1680609600, 'main': {'temp': 4.37, 'feels_like': 0.87, 'temp_min': 4.37, 'temp_max': 5.2, 'pressure': 1017, 'sea_level': 1017, 'grnd_level': 929, 'humidity': 50, 'temp_kf': -0.83}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'clouds': {'all': 44}, 'wind': {'speed': 4.37, 'deg': 56, 'gust': 5.88}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2023-04-04 12:00:00'}, {'dt': 1680620400, 'main': {'temp': 4.64, 'feels_like': 1.51, 'temp_min': 4.64, 'temp_max': 4.99, 'pressure': 1016, 'sea_level': 1016, 'grnd_level': 928, 'humidity': 45, 'temp_kf': -0.35}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'clouds': {'all': 17}, 'wind': {'speed': 3.84, 'deg': 65, 'gust': 5.39}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2023-04-04 15:00:00'}, {'dt': 1680631200, 'main': {'temp': 0.11, 'feels_like': 0.11, 'temp_min': 0.11, 'temp_max': 0.11, 'pressure': 1017, 'sea_level': 1017, 'grnd_level': 928, 'humidity': 59, 
'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 1}, 'wind': {'speed': 0.34, 'deg': 335, 'gust': 1.27}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2023-04-04 18:00:00'}, {'dt': 1680642000, 'main': {'temp': -0.86, 'feels_like': -0.86, 'temp_min': -0.86, 'temp_max': -0.86, 'pressure': 1019, 'sea_level': 1019, 'grnd_level': 930, 'humidity': 55, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 0}, 'wind': {'speed': 1.01, 'deg': 228, 'gust': 1.43}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2023-04-04 21:00:00'}, {'dt': 1680652800, 'main': {'temp': -1.24, 'feels_like': -1.24, 'temp_min': -1.24, 'temp_max': -1.24, 'pressure': 1020, 'sea_level': 1020, 'grnd_level': 930, 'humidity': 64, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': 
'01n'}], 'clouds': {'all': 2}, 'wind': {'speed': 1.23, 'deg': 210, 'gust': 1.87}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2023-04-05 00:00:00'}, {'dt': 1680663600, 'main': {'temp': -1.58, 'feels_like': -1.58, 'temp_min': -1.58, 'temp_max': -1.58, 'pressure': 1019, 'sea_level': 1019, 'grnd_level': 929, 'humidity': 63, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'clouds': {'all': 3}, 'wind': {'speed': 1.28, 'deg': 234, 'gust': 2.21}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2023-04-05 03:00:00'}, {'dt': 1680674400, 'main': {'temp': 0.11, 'feels_like': 0.11, 'temp_min': 0.11, 'temp_max': 0.11, 'pressure': 1019, 'sea_level': 1019, 'grnd_level': 930, 'humidity': 
59, 'temp_kf': 0}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'clouds': {'all': 3}, 'wind': {'speed': 0.64, 'deg': 167, 'gust': 4.83}, 'visibility': 
10000, 'pop': 0, 'sys': {'pod': 'd'}, 'dt_txt': '2023-04-05 06:00:00'}], 'city': {'id': 3163858, 'name': 'Zocca', 'coord': {'lat': 44.34, 'lon': 10.99}, 'country': 'IT', 'population': 4593, 'timezone': 7200, 'sunrise': 1680583945, 'sunset': 1680630330}}

def example_call() -> str:
    return get_weather(44.34, 10.99)

def get_weather(lat: float, lon:float) -> str:
    return get_current_weather(lat, lon) + " " + get_weather_forecast(lat, lon)

def get_current_weather(lat: float, lon:float) -> str:
    url = f"{base_url}/weather?lat={lat}&lon={lon}&units=metric&appid={APIKEY}"
    response = requests.get(url)
    data = response.json()
    city = data["name"]
    weather = data["weather"][0]["description"]
    if weather == "clear sky":
        weather = "clear skies"
    temp = int(round(data["main"]["temp"], 0))
    return f"It is currently {temp} degrees celsius in {city} with {weather}."

def get_weather_forecast(lat: float, lon:float) -> str:
    url = f"{base_url}/forecast?lat={lat}&lon={lon}&units=metric&cnt=8&appid={APIKEY}"
    # response = requests.get(url)
    # data = response.json()
    data = data_cache
    temps = []
    descriptions = []
    date = data["list"][0]["dt_txt"].split(' ')[0]
    for timestamp in data["list"]:
        if timestamp["dt_txt"].split(' ')[0] == date:
            temp = int(round(timestamp["main"]["temp"], 0))
            temps.append(temp)
            descriptions.append(timestamp["weather"][0]["description"])

    min_temp = min(temps)
    max_temp = max(temps)
    afternoon_weather = descriptions[-2] if len(descriptions)>2 else descriptions[-1]
    if afternoon_weather == "clear sky":
        afternoon_weather = "clear skies"
    return f"Today, the forecast calls for a low of {min_temp} and a high of {max_temp} degrees, with {afternoon_weather} in the afternoon."
