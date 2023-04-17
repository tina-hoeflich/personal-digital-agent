from justwatch import JustWatch

def find_on_netflix(popular_movies):
    just_watch = JustWatch(country='DE')
    movies_on_netflix = {}
    movies_not_on_netflix = []

    for movie in popular_movies:
        link_and_poster_list = []
        results = just_watch.search_for_item(query=movie.title, content_types=['movie'])
        results = results['items']
        if len(results) > 0:
            title = results[0]['title']
            if 'offers' in results[0]:
                netflix_available = any(provider['provider_id'] == 8 for provider in results[0]['offers'])
                if netflix_available:
                    netflix_link = next(provider['urls']['standard_web'] for provider in results[0]['offers'] if provider['provider_id'] == 8)
                    link_and_poster_list.append(netflix_link)
                    link_and_poster_list.append(movie.poster_path)
                    movies_on_netflix[title] = link_and_poster_list
                else:
                    movies_not_on_netflix.append(title)
            else:
                movies_not_on_netflix.append(title)
    
    return movies_on_netflix, movies_not_on_netflix