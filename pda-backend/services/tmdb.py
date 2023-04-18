from tmdbv3api import TMDb, Movie
import requests
from PIL import Image
from io import BytesIO
import os

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

def get_popular_movies() -> list:
    """This method gets the 20 most popular movies from the tmdb api.

    Returns:
        list: list of 20 popular movies
    """    
    tmdb = TMDb()
    tmdb.api_key = TMDB_API_KEY
    tmdb.language = 'en'
    tmdb.debug = True

    movie = Movie()
    popular_movies = movie.popular()
    return popular_movies

def get_movie_poster(poster_path: str) -> str:
    """This method gets the link to a poster of a movie from tmdb.

    Args:
        poster_path (str): path to the poster

    Returns:
        str:  link to the poster
    """    
    # response = requests.get(f"https://image.tmdb.org/t/p/w500/{poster_path}")
    # with Image.open(BytesIO(response.content)) as im:
    #     im.show()
    return f"https://image.tmdb.org/t/p/w500/{poster_path}"
