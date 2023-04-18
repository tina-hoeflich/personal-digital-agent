import random
from datetime import datetime, timedelta

import services.tmdb as tmdb
import services.justwatch as justwatch
import services.calender as calender

from usecases.usecase import UseCase
from scheduler import Scheduler
from settings_manager import SettingsManager
from proaktiv_sender import ProaktivSender
from conversation_manager import ConversationManager
from kink import inject
from typing import Callable

TRIGGERS = ["movie", "netflix", "chill", "watch", "stream", "streaming", "cinema", "film"]

@inject
class NetflixAndChillUseCase(UseCase):
    def __init__(self, scheduler: Scheduler, settings: SettingsManager, proaktive: ProaktivSender, conv_man: ConversationManager):
        self.scheduler = scheduler
        self.settings = settings
        self.proaktive = proaktive
        self.conv_man = conv_man
        self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(minutes=1))

    def get_triggerwords(self) -> list[str]:
        return TRIGGERS
    
    def trigger(self):
        self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(minutes=10))

        last_event_name, last_event_end_time, new_time = calender.get_last_event()

        if last_event_name == None:
            text_possibilities = ["You have no classes today. Do you want to watch a movie now?",
                                    "Hey, looks like you have a free day with no classes! How about catching a movie?",
                                    "Good news! There are no classes today. Want to make the most of it and watch a movie?",
                                    "Guess what? You're off the hook from classes today. Want to unwind and watch a movie?"]
            text = random.choice(text_possibilities)
            self.proaktive.send_text(text)
        else:
            text_possibilities = [f"Your last class today is {last_event_name} and it ends at {last_event_end_time}. Do you want to watch a movie at {new_time}.",
                                    f"After {last_event_name} ends at {last_event_end_time}, you'll have some free time. Do you want to watch a movie at {new_time}?",
                                    f"Your final class for today, {last_event_name}, ends at {last_event_end_time}. How about catching a movie at {new_time}?",
                                    f"Just a reminder, {last_event_name} wraps up at {last_event_end_time}. Are you interested in watching a movie at {new_time}?"]
            text = random.choice(text_possibilities)
            self.proaktive.send_text(text)

        self.conv_man.set_net_method(self.conversation)
    
    async def asked(self, input: str) -> tuple[str, Callable]:
        text, poster_link, movie_link = self.get_movie_recommendation()
        return text, None, poster_link, movie_link
    
    def conversation(self, input: str) -> tuple[str, Callable or None]:
        if " no " in " " + input.lower() + " ":
            text_possibilities = ["Okay, maybe next time.",
                                    "That's okay. Want anything else.",
                                    "Alright. I'm here if you need me"]
            return random.choice(text_possibilities), None
        
        text, poster_link, movie_link = self.get_movie_recommendation()
        return text, None, poster_link, movie_link
    
    def get_movie_recommendation(self) -> str:
        popular_movies = tmdb.get_popular_movies()
        movies_on_netflix, movies_not_on_netflix = justwatch.find_on_netflix(popular_movies)
        movie_title, movie_link = random.choice(list(movies_on_netflix.items()))
        poster_link = tmdb.get_movie_poster(movies_on_netflix[movie_title][1])

        text_possibilities = [f"Great! {movie_title} is available on Netflix! Watch it here: {movie_link[0]}",
                                    f"Awesome news! {movie_title} is now streaming on Netflix. Catch it here: {movie_link[0]}",
                                    f"Exciting update! {movie_title} is now accessible on Netflix. Don't miss it! Watch it here: {movie_link[0]}",
                                    f"Good news! {movie_title} is now playing on Netflix. Don't wait, click here to watch it: {movie_link[0]}"]
        text = random.choice(text_possibilities)

        return text, poster_link, movie_link[0]
        
    def get_settings(self) -> object:
        return self.settings.get_setting_by_name("example")