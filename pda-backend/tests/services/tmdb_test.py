import services.tmdb as tmdb

def test_get_popular_movies():
    popular_movies = tmdb.get_popular_movies()
    
    assert len(popular_movies) == 20
    for movie in popular_movies:
        assert "id" in movie
        assert "title" in movie
        assert "poster_path" in movie

def test_get_movie_poster():
    poster_path = "/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg"
    expected_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    
    actual_url = tmdb.get_movie_poster(poster_path)
    
    assert actual_url == expected_url
