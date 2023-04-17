import os
import requests

APIKEY = os.environ.get("WEATHER_API_KEY")
base_url = "https://api.openweathermap.org/data/2.5"

def get_weather_code(lat: float, lng: float) -> int:
    """
    get_weather_code gets the openweathermap weather condition code. More info can be found here https://openweathermap.org/weather-conditions

    Args:
        lat (float): latitude
        lng (float): longitude

    Raises:
        Exception: unsuccessful api call data

    Returns:
        int: weather code
    """
    url = f"{base_url}/weather?lat={lat}&lon={lng}&units=metric&appid={APIKEY}"
    response = requests.get(url)
    data = response.json()
    if(data["cod"] != 200):
        raise Exception(data["message"])

    weather = data["weather"][0]["id"]
    return weather

def get_current_weather(lat: float, lng: float) -> tuple[int, str, str]:
    """
    get_current_weather returns multiple variables describing the current weather at a given location

    Args:
        lat (float): latitude
        lng (float): longitude

    Raises:
        Exception: unsuccessful api call data

    Returns:
        tuple[int, str, str]: temperature, city name, weather description
    """
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
    return temp, city, weather
    return f""

def get_weather_forecast(lat: float, lng: float) -> tuple[int, int, str]:
    """
    get_weather_forecast returns multiple variables describing the weather forecast for the rest of the current day

    Args:
        lat (float): latitude
        lng (float): longitude

    Returns:
        tuple[int, int, str]: lowest temperature today, highest temperature today, weather description at 18:00 
    """
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
    return min_temp, max_temp, afternoon_weather