from usecases.usecase import UseCase
from scheduler import Scheduler
import services.weather as weather
import services.news as news
import services.maps as maps
import services.geolocation as geolocation
from settings_manager import SettingsManager
from proaktiv_sender import ProaktivSender
from typing import Callable
from datetime import datetime, timedelta
import random
import math
from kink import inject

GENERAL_TRIGGERS = ["morning", "day", "rise", "alarm"]
HELP_TRIGGERS = ["help", "know", "how"]
WEATHER_TRIGGERS = ["weather", "temperature", "warm", "cold", "rain", "rainy", "sunny", "sun", "cloud", "clouds", "cloudy"]
NEWS_TRIGGERS = ["news", "update", "updates", "story", "stories", "message", "messages"]
MAPS_TRIGGERS = ["directions", "car", "walk", "bike", "drive", "leave", "work"]

AFFIRM_TRIGGERS = ["yes", "sure", "okay", "ok", "fine", "gladly"]
CANCEL_TRIGGERS = ["no", "nothing", "bye", "stop", "usecase", "never"]

@inject
class GutenMorgenUseCase(UseCase):
	alternate_travel_mode = None
	def __init__(self, scheduler: Scheduler, settings: SettingsManager, proaktive: ProaktivSender):
		self.scheduler = scheduler
		self.settings = settings
		self.proaktive = proaktive
		self.trigger()

	def get_triggerwords(self) -> list[str]:
		return GENERAL_TRIGGERS

	def trigger(self):
		"""
		trigger On app start, schedules self.alarm to execute 30 minutes before work_time - travel_time
		"""
		cached_travel_time = self.get_cached_travel_time()
		time_to_get_ready = 30
		self.scheduler.schedule_job(self.alarm, self.get_work_time() - timedelta(minutes=cached_travel_time) - timedelta(minutes=time_to_get_ready) )
	
	def alarm(self):
		"""
		alarm PROACTIVE USECASE. Wakes user up and tells him when he needs to leave for work
		"""
		self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(minutes=10))

		cached_travel_time = self.get_cached_travel_time()
		work_time = self.get_work_time()
		leave_time = work_time - timedelta(minutes=cached_travel_time) - timedelta(minutes=5)
		text = f"{self.greeting()} You should leave at {leave_time.strftime('%H:%M')} to get to work at {work_time.strftime('%H:%M')} on time!"
		self.proaktive.send_text(text)
	
	def get_work_time(self) -> datetime:
		"""
		get_work_time returns the time when the user has work. Currently mock function always returns 9:00 the next day. Should integrate with rapla service

		Returns:
			datetime: Time when work starts
		"""
		now = datetime.now()
		work_time = now
		hour = now.hour
		if hour < 9:
			work_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
		else:
			work_time = now.replace(day=now.day+1, hour=9, minute=0, second=0, microsecond=0)
		return work_time

	async def asked(self, input: str) -> tuple[str, Callable]:
		"""
		asked Entry function for gutenmorgen usecase. Gives greeting and moves on to conversation

		Args:
			input (str): str input from frontend

		Returns:
			tuple[str, Callable]: frontend output, converstation function
		"""
		return self.greeting() + " " + self.start_question(), self.conversation
	
	def conversation(self, input: str) -> tuple[str, Callable]:
		"""
		conversation main menu of sorts for guten morgen usecase. Can navigate to each service from here

		Args:
			input (str): frontend input 

		Returns:
			tuple[str, Callable]: frontend output, internal service function
		"""
		input = input.split(" ")
		if any(trigger in input for trigger in CANCEL_TRIGGERS):
			return "Okay. See you later!", None
		if any(trigger in input for trigger in HELP_TRIGGERS):
			return "I can tell you about the weather, the news nad your commute, or you can try another usecase by saying bye!", self.conversation
		if any(trigger in input for trigger in WEATHER_TRIGGERS):
			return self.weather() + " " + self.repeat_question(), self.conversation
		if any(trigger in input for trigger in NEWS_TRIGGERS):
			return self.news_title(), self.news_conversation
		if any(trigger in input for trigger in MAPS_TRIGGERS):
			text, self.alternate_travel_mode = self.travel_helper()
			if self.alternate_travel_mode:
				return text, self.travel_alternate_conversation
			else:
				return f"{text} {self.repeat_question()}", self.conversation
		
		return "I didn't understand you. " + self.repeat_question(), self.conversation

	def greeting(self) -> str:
		"""
		greeting returns a greeting to the user with his name

		Returns:
			str: random greeting
		"""
		name = self.get_settings()["name"]
		greetings = [
			f"Good Morning {name}, let's get your day started!",\
			f"Welcome back {name}.",\
			f"Good Morning {name}.",\
			f"Rise and shine {name}! I'm here and ready to help."]
		return random.choice(greetings)
	
	def start_question(self) -> str:
		"""
		start_question returns a question prompt to the user

		Returns:
			str: questino prompt
		"""
		questions = [
			"What would you like to do?",\
			"How may i help you today?",\
			"Please let me know how I can assist you today.",\
			"What can I do for you?",\
			"How can I be of service today?.",\
			"What would you like to know about?"]
		return random.choice(questions)
	
	def repeat_question(self) -> str:
		"""
		repeat_question returns a repeat questino prompt

		Returns:
			str: repeat question prompt
		"""
		questions = [
			"Would you like to know anything else?",\
			"What else can I help you with?",\
			"Can I help you with anything else?",\
			"What else can I do for you?",\
			"How else can I be of service?.",\
			"Would you like to know anything else?"]
		return random.choice(questions)

	def weather(self) -> str:
		"""
		weather returns a detailed description of the current weather and daily forecast

		Returns:
			str: weather description
		"""
		settings = self.get_settings()
		home_address = settings["homeAddress"]
		lat, lng = geolocation.get_location_from_address(home_address)
		temp, city, description = weather.get_current_weather(lat, lng)
		min_temp, max_temp, afternoon_description = weather.get_weather_forecast(lat, lng)
		return f"It is currently {temp} degrees celsius in {city} with {description}. \
				Today, the forecast calls for a low of {min_temp} and a high of {max_temp} degrees, with {afternoon_description} in the afternoon."

	def news_title(self) -> str:
		"""
		news_title returns a title of a news story plus some text introducing and preceding the title

		Returns:
			str: formatted text of news title
		"""
		intros = [
			"Sure, here's the latest story: ",\
			"Sure, here's the latest scoop: ",\
			"Okay, here's a story I found: ",\
			"I found this story for you: ",\
			"This might be interesting: ",\
			"Sure, I found this story for you: ",\
		]
		outros = [
			"Would you like more information on this story?",\
			"Would you like to know more about this story?",\
			"Would you like to hear more?",\
			"Should I tell you more about this article?",\
			"Would you like to know more?",\
			"Would you like more information?"
		]
		return f"{random.choice(intros)} {news.get_news_title()}. {random.choice(outros)}"
	
	def news_conversation(self, input: str) -> tuple[str, Callable]:
		"""
		news_conversation news service submenu. Asks the user if he would like more information about the story

		Args:
			input (str): frontend input

		Returns:
			tuple[str, Callable]: frontend output, conversation function
		"""
		if any(trigger in input for trigger in AFFIRM_TRIGGERS):
			return f"{news.get_news_content()} {self.repeat_question()}", self.conversation
		
		return f"Okay. {self.repeat_question()}", self.conversation
	
	def travel_helper(self) -> tuple[str, str]:
		"""
		travel_helper gives the user the current time required to get to work. Suggests different method of travel based on weather conditions

		Returns:
			tuple[str, str]: frontend output, alternate mode of transportation
		"""
		settings = self.get_settings()
		mode = settings["modeOfTransportation"]
		text = self.travel_time_format(mode)

		home_address = settings["homeAddress"]
		lat, lng = geolocation.get_location_from_address(home_address)
		weather_code = weather.get_weather_code(lat, lng)
		
		if(weather_code < 800 and mode in ["bicycling", "walking"]):
			text += " But the weather today seems pretty bad, maybe you'd like to drive instead?"
			return text, "driving"
		elif(weather_code >= 800 and mode == "driving"):
			text += " The weather today looks great! Maybe you'd like to cycle instead?"
			return text, "bicycling"
		else:
			return text, None
		
	def travel_alternate_conversation(self, input: str) -> tuple[str, Callable]:
		"""
		travel_alternate_conversation maps service submenu. Asks if user would like to change travel method.

		Args:
			input (str): frontend input 

		Returns:
			tuple[str, Callable]: frontend output, conversation function 
		"""
		if any(trigger in input for trigger in AFFIRM_TRIGGERS):
			return f"Okay. {self.travel_time_format(self.alternate_travel_mode)} {self.repeat_question()}", self.conversation
		
		return f"Okay. {self.repeat_question()}", self.conversation
	
	def travel_time_format(self, mode: str) -> str:
		"""
		travel_time_format formats the time to travel to sound nice with introduction and preceding string

		Args:
			mode (str): mode of trasportation

		Returns:
			str: travel time with intro and outro 
		"""
		time = self.get_travel_time(mode)
		# time = self.get_cached_travel_time()
		intros = [
			"If you leave now, you will need",
			"Leaving now, it will take",
			"Based on current traffic, it will take",
			"Currently, you'll need",
			"At the moment, you will need",
			"Right now, you'll need"
		]
		return f"{random.choice(intros)} {time} minutes to get to work by {mode}."

	def get_cached_travel_time(self) -> int:
		"""
		get_cached_travel_time returns the travel time from the maps cache. Should only be used for repeating tasks like the scheduler

		Returns:
			int: travel time in minutes
		"""
		settings = self.get_settings()
		origin = settings["homeAddress"]
		destination = settings["workAddress"]
		transportation = settings["modeOfTransportation"]
		time = maps.get_cached_travel_time(origin, destination, transportation)
		return int(round(time/60, 0))

	def get_travel_time(self, transportation: str) -> int:
		"""
		get_travel_time returns the current travel time from the maps api. Used for getting current data

		Args:
			transportation (str): mode of transportation

		Returns:
			int: travel time in minutes
		"""
		settings = self.get_settings()
		origin = settings["homeAddress"]
		destination = settings["workAddress"]
		
		time = maps.get_current_travel_time(origin, destination, transportation)
		return int(round(time/60, 0))

	def get_settings(self) -> dict:
		"""
		get_settings returns settings of the goodMorning usecase

		Returns:
			dict: settings dictionary 
		"""
		return self.settings.get_setting_by_name("goodMorning")
