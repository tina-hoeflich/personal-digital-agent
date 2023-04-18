from justwatch import JustWatch

def find_on_netflix(popular_movies: list) -> tuple[dict, list]:
    """This method finds the movies from the popular list which are on netflix.

    Args:
        popular_movies (list): list of 20 popular movies

    Returns:
        tuple[dict, list]: dictionary of movies on netflix with lniks and poster links and list of movies not on netflix
    """    
    just_watch = JustWatch(country='DE')
    movies_on_netflix = {}
    movies_not_on_netflix = []

    for movie in popular_movies:
        link_and_poster_list = []
        search_results = just_watch.search_for_item(query=movie.title, content_types=['movie'])
        search_results = search_results['items']

        if len(search_results) > 0:
            movie_title = search_results[0]['title']

            if 'offers' in search_results[0]:
                netflix_available = any(provider['provider_id'] == 8 for provider in search_results[0]['offers'])

                if netflix_available:
                    netflix_link = next(provider['urls']['standard_web'] for provider in search_results[0]['offers'] if provider['provider_id'] == 8)
                    link_and_poster_list.append(netflix_link)
                    link_and_poster_list.append(movie.poster_path)
                    movies_on_netflix[movie_title] = link_and_poster_list
                else:
                    movies_not_on_netflix.append(movie_title)
                    
            else:
                movies_not_on_netflix.append(movie_title)
    
    return movies_on_netflix, movies_not_on_netflix