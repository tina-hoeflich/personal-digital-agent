import os
import json
import googlemaps
from datetime import datetime

GOOGLE_MAPS_API_KEY=os.environ.get("GOOGLE_MAPS_API_KEY")

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

maps_cache_file = os.path.join('resources', 'maps_cache.json')

def get_and_refresh_cache(frm: str, to:str, mode:str) -> dict:
    """
    get_and_refresh_cache gets the maps directions data from the cache (maps_cache.json). If the input parameters have changed or the cache is more than 3 hours old, refreshes the cache

    Args:
        frm (str): travel origin
        to (str): travel destination
        mode (str): mode of transportation

    Returns:
        dict: data from maps_cache
    """
    current_date = datetime.today().strftime('%Y-%m-%d')
    current_hour = datetime.now().hour

    cache_data = {}
    cache_params = {}
    try:
        cache = open(maps_cache_file, "r")
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
    """
    refresh_cache overwrites the cache with a new dictionary object

    Args:
        data (dict): new maps directions data
    """
    print("refreshing maps_cache...")
    json_data = json.dumps(data, indent=4)
    cache = open(maps_cache_file, "w")
    cache.write(json_data) 

def get_current_data(frm: str, to: str, mode:str) -> dict:
    """
    get_current_data calls the google maps direction api and returns the direction data

    Args:
        frm (str): travel origin
        to (str): travel destination
        mode (str): mode of transportation

    Returns:
        dict: maps direction data
    """
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
    if res == []:
        raise Exception('could not get travel data!')
    return data

def get_cached_travel_time(origin: str, destination: str, mode_of_transportation: str) -> int:
    """
    get_cached_travel_time gets the travel time from the maps cache (maps_cache.json)

    Args:
        origin (str): travel origin
        destination (str): travel destination
        mode_of_transportation (str): mode of transportation

    Returns:
        int: travel time in seconds
    """
    cache = get_and_refresh_cache(origin, destination, mode_of_transportation)
    if(mode_of_transportation == "driving"):
        return cache["data"][0]["legs"][0]["duration_in_traffic"]["value"]
    return cache["data"][0]["legs"][0]["duration"]["value"]

def get_current_travel_time(origin: str, destination: str, mode_of_transportation: str) -> int:
    """
    get_current_travel_time gets the travel time from a new google maps directions api call. Refreshes the cache with that data

    Args:
        origin (str): travel origin
        destination (str): travel destination
        mode_of_transportation (str): mode of transportation

    Returns:
        int: travel time in seconds
    """
    data = get_current_data(origin, destination, mode_of_transportation)
    refresh_cache(data)
    if(mode_of_transportation == "driving"):
        return data["data"][0]["legs"][0]["duration_in_traffic"]["value"]
    return data["data"][0]["legs"][0]["duration"]["value"]
