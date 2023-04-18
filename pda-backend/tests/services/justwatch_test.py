import services.justwatch as justwatch
import services.tmdb as tmdb

def test_find_on_netflix():
    popular_movies = tmdb.get_popular_movies()
    movies_on_netflix, movies_not_on_netflix = justwatch.find_on_netflix(popular_movies)
    
    assert type(movies_on_netflix) == dict
    assert type(movies_not_on_netflix) == list
    assert len(movies_on_netflix) >= 1
    assert len(movies_not_on_netflix) >= 2