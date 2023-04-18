from tmdbv3api import TMDb, Movie
import requests
from PIL import Image
from io import BytesIO
import os

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

def get_popular_movies():
    tmdb = TMDb()
    tmdb.api_key = TMDB_API_KEY
    tmdb.language = 'en'
    tmdb.debug = True

    movie = Movie()
    popular_movies = movie.popular()
    return popular_movies

def get_movie_poster(poster_path):
    # response = requests.get(f"https://image.tmdb.org/t/p/w500/{poster_path}")
    # with Image.open(BytesIO(response.content)) as im:
    #     im.show()
    return f"https://image.tmdb.org/t/p/w500/{poster_path}"
