import os
import json
import requests
import random

APIKEY = os.environ.get("NEWS_API_KEY")
url = f"https://newsdata.io/api/1/news?language=en&country=de&apikey={APIKEY}"
story_num = 0

news_cache = {}

def get_news() -> str:
    return "Nothing new!"

def get_news_title() -> str:
    global news_cache
    global story_num
    if news_cache == {}:
        news_cache = open("news_cache.json", "r", encoding="utf8").read()
    
    news_cache = json.loads(news_cache)

    story_num = random.randint(0, 9)
    return news_cache["results"][story_num]["title"]

def get_news_content() -> str:
    global news_cache
    return news_cache["results"][story_num]["description"]

print(get_news_title(), get_news_content())