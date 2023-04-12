import os
import json
import requests
import random

# APIKEY = os.environ.get("NEWS_API_KEY")
APIKEY = "pub_20412ce418b757cf39d74d52d4de9acd4f3e9"
news_sources = "insider,cnn,cbsnews,wired,nbcnews"
url = f"https://newsdata.io/api/1/news?language=en&country=us&domain={news_sources}&apikey={APIKEY}"
story_num = 0

news_cache = {}

def get_news_title() -> str:
    global news_cache
    global story_num
    if news_cache == {}:
        response = requests.get(url)
        news_cache = response.json()
    
    print(url)
    print(news_cache)
    story_num = random.randint(0, 9)
    return news_cache["results"][story_num]["title"]

def get_news_content() -> str:
    global news_cache
    return news_cache["results"][story_num]["description"]