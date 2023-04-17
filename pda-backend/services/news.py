import os
import json
import requests
import random

APIKEY = os.environ.get("NEWS_API_KEY")
news_sources = "insider,cnn,wired,nbcnews,wsj"
url = f"https://newsdata.io/api/1/news?language=en&country=us&domain={news_sources}&apikey={APIKEY}"
story_num = 0

news_cache = {}

def get_news_title() -> str:
    """
    get_news_title Calls the news api and saves results in cache. 
    Returns the title of a random story, saves num in global story_num for other functions

    Returns:
        str: _description_
    """
    global news_cache
    global story_num
    if news_cache == {}:
        response = requests.get(url)
        news_cache = response.json()
    
    story_num = random.randint(0, 9)
    return news_cache["results"][story_num]["title"]

def get_news_content() -> str:
    """
    get_news_content Calls the news api and saves the results in cache. 
    Returns the description of a story defined by global story_num set in get_news_title
    Should call after calling get_news_title()

    Returns:
        str: news story description
    """
    global news_cache
    global story_num
    if news_cache == {}:
        response = requests.get(url)
        news_cache = response.json()
    
    return news_cache["results"][story_num]["description"]