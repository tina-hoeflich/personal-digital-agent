from tmdbv3api import TMDb, Movie
import requests
from PIL import Image
from io import BytesIO

def get_popular_movies():
    tmdb = TMDb()
    tmdb.api_key = 'b3e56fddd812de48269710ffd2f749e4'
    tmdb.language = 'en'
    tmdb.debug = True

    movie = Movie()
    popular_movies = movie.popular()
    return popular_movies

def get_movie_poster(poster_path):
    show_image = True
    response = requests.get(f"https://image.tmdb.org/t/p/w500/{poster_path}")
    if show_image:
        with Image.open(BytesIO(response.content)) as im:
            im.show()
