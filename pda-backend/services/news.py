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
    global news_cache
    global story_num
    if news_cache == {}:
        response = requests.get(url)
        news_cache = response.json()
    
    story_num = random.randint(0, 9)
    return news_cache["results"][story_num]["title"]

def get_news_content() -> str:
    global news_cache
    return news_cache["results"][story_num]["description"]