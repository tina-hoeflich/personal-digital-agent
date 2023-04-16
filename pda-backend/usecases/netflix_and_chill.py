import random

import services.tmdb as tmdb
import services.justwatch as justwatch
import services.calender as calender

from usecases.usecase import UseCase
from scheduler import Scheduler
from settings_manager import SettingsManager
from kink import inject
from typing import Callable

TRIGGERS = ["movie", "netflix", "chill", "watch", "stream", "streaming", "cinema", "film"]

@inject
class NetflixAndChillUseCase(UseCase):
    def __init__(self, scheduler: Scheduler, settings: SettingsManager):
        self.scheduler = scheduler
        self.settings = settings

    def get_triggerwords(self) -> list[str]:
        return TRIGGERS
    
    def trigger(self):
		# hier kommt das periodische checken für proaktive Dinge rein.

		# hier muss jeder trigger noch den nächsten run schedulen
        return
    
    async def asked(self, input: str) -> tuple[str, Callable]:
        return self.get_movie_recommendation(), None
    
    def get_movie_recommendation(self) -> str:
        last_event_name, last_event_end_time, new_time = calender.get_last_event()
        popular_movies = tmdb.get_popular_movies()
        movies_on_netflix, movies_not_on_netflix = justwatch.find_on_netflix(popular_movies)
        movie, link = random.choice(list(movies_on_netflix.items()))
        tmdb.get_movie_poster(movies_on_netflix[movie][1])
        if last_event_name == None:
            return f"You have no classes today. {movie} is available on Netflix! Watch it here: {link[0]}"
        else:
            return f"Your last class today is {last_event_name} and it ends at {last_event_end_time}. So you have time to watch a movie at {new_time}. {movie} is available on Netflix! Watch it here: {link[0]}", None,  link[0]
        
    def get_settings(self) -> object:
        return self.settings.get_setting_by_name("example")