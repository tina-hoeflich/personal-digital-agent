import os
import requests

APIKEY = os.environ.get("WEATHER_API_KEY")
base_url = "https://api.openweathermap.org/data/2.5"


def get_weather(lat: float, lng:float) -> str:
    
    return get_current_weather(lat, lng) + " " + get_weather_forecast(lat, lng)

def get_weather_code(lat: float, lng: float) -> str:
    url = f"{base_url}/weather?lat={lat}&lon={lng}&units=metric&appid={APIKEY}"
    response = requests.get(url)
    data = response.json()
    if(data["cod"] != 200):
        raise Exception(data["message"])

    weather = data["weather"][0]["id"]
    return weather

def get_current_weather(lat: float, lng: float) -> str:
    url = f"{base_url}/weather?lat={lat}&lon={lng}&units=metric&appid={APIKEY}"
    response = requests.get(url)
    data = response.json()
    # print(data["cod"])
    if(data["cod"] != 200):
        raise Exception(data["message"])

    city = data["name"]
    weather = data["weather"][0]["description"]
    if weather == "clear sky":
        weather = "clear skies"
    temp = int(round(data["main"]["temp"], 0))
    return f"It is currently {temp} degrees celsius in {city} with {weather}."

def get_weather_forecast(lat: float, lng: float) -> str:
    url = f"{base_url}/forecast?lat={lat}&lon={lng}&units=metric&appid={APIKEY}"
    response = requests.get(url)
    data = response.json()

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