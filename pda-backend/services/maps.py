import os
import json
import googlemaps
from datetime import datetime

GOOGLE_MAPS_API_KEY=os.environ.get("GOOGLE_MAPS_API_KEY")

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def get_and_refresh_cache(frm: str, to:str, mode:str) -> dict:
    current_date = datetime.today().strftime('%Y-%m-%d')
    current_hour = datetime.now().hour

    cache_data = {}
    cache_params = {}
    try:
        cache = open(f"{os.getcwd()}{os.sep}maps_cache.json", "r")
        cache_data = json.load(cache)
        cache_params = cache_data["parameters"]
    except:
        print("could not find maps_cache file. Creating new...")
        cache_params = {
            "origin": "",
            "destination": "",
            "mode": "",
            "date": "",
            "hour": 0,
        }
    
    if(
        cache_params["date"] != current_date 
        # or abs(cache_params["hour"]-current_hour) > 3 
        or cache_params["origin"] != frm
        or cache_params["destination"] != to
        or cache_params["mode"] != mode
        ):
        cache_data = get_current_data(frm, to, mode)
        refresh_cache(cache_data)
    
    return cache_data

def refresh_cache(data: dict) -> None:
    print("refreshing maps_cache...")
    json_data = json.dumps(data, indent=4)
    cache = open(f"{os.getcwd()}{os.sep}maps_cache.json", "w")
    cache.write(json_data) 

def get_current_data(frm: str, to: str, mode:str) -> dict:
    print("calling maps api...")
    current_date = datetime.today().strftime('%Y-%m-%d')
    current_hour = datetime.now().hour
    res = gmaps.directions(origin=frm, destination=to, mode=mode, departure_time=datetime.now())
    data = {
        "parameters": {
            "origin": frm,
            "destination": to,
            "mode": mode,
            "date": current_date,
            "hour": current_hour,
        }, 
        "data": res
    }
    return data

def get_cached_travel_time(origin: str, destination: str, mode_of_transportation: str) -> int:
    cache = get_and_refresh_cache(origin, destination, mode_of_transportation)
    if(mode_of_transportation == "driving"):
        return cache["data"][0]["legs"][0]["duration_in_traffic"]["value"]
    return cache["data"][0]["legs"][0]["duration"]["value"]

def get_current_travel_time(origin: str, destination: str, mode_of_transportation: str) -> int:
    data = get_current_data(origin, destination, mode_of_transportation)
    refresh_cache(data)
    if(mode_of_transportation == "driving"):
        return data["data"][0]["legs"][0]["duration_in_traffic"]["value"]
    return data["data"][0]["legs"][0]["duration"]["value"]
