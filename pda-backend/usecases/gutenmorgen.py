from usecases.usecase import UseCase
from scheduler import Scheduler
from services.weather import get_weather
from services.news import get_news_title, get_news_content
import services.geolocation as geolocation
from settings_manager import SettingsManager
from typing import Callable
import random
from kink import inject

GENERAL_TRIGGERS = ["morning", "day", "rise", "alarm"]
HELP_TRIGGERS = ["help", "know", "how"]
WEATHER_TRIGGERS = ["weather", "temperature", "warm", "cold", "rain", "rainy", "sunny", "sun", "cloud", "clouds", "cloudy"]
NEWS_TRIGGERS = ["news", "update", "updates", "story", "stories", "message", "messages"]

AFFIRM_TRIGGERS = ["yes", "sure", "okay", "fine", "gladly"]
CANCEL_TRIGGERS = ["no", "nothing", "bye", "leave", "stop", "usecase", "never"]

@inject
class GutenMorgenUseCase(UseCase):
	def __init__(self, scheduler: Scheduler, settings: SettingsManager):
		self.scheduler = scheduler
		self.settings = settings

	def get_triggerwords(self) -> list[str]:
		return GENERAL_TRIGGERS

	def trigger(self):
		# hier kommt das periodische checken für proaktive Dinge rein.

		# hier muss jeder trigger noch den nächsten run schedulen
		return

	async def asked(self, input: str) -> tuple[str, Callable]:
		return self.greeting() + " " + self.start_question(), self.conversation
	
	def conversation(self, input: str) -> tuple[str, Callable]:
		input = input.split(" ")
		if any(trigger in input for trigger in CANCEL_TRIGGERS):
			return "Okay. See you later!", None
		if any(trigger in input for trigger in HELP_TRIGGERS):
			return "I can tell you about the weather or the news, or you can try another usecase by saying bye!", self.conversation
		if any(trigger in input for trigger in WEATHER_TRIGGERS):
			return self.weather() + " " + self.repeat_question(), self.conversation
		if any(trigger in input for trigger in NEWS_TRIGGERS):
			return self.news_title(), self.news_conversation
		
		return "I didn't understand you. " + self.repeat_question(), self.conversation

	def greeting(self) -> str:
		name = self.get_settings()["name"]
		greetings = [
			f"Good Morning {name}, let's get your day started!",\
			f"Welcome back {name}.",\
			f"Good Morning {name}.",\
			f"Rise and shine {name}! I'm here and ready to help."]
		return random.choice(greetings)
	
	def start_question(self) -> str:
		questions = [
			"What would you like to do?",\
			"How may i help you today?",\
			"Please let me know how I can assist you today.",\
			"What can I do for you?",\
			"How can I be of service today?.",\
			"What would you like to know about?"]
		return random.choice(questions)
	
	def repeat_question(self) -> str:
		questions = [
			"Would you like to know anything else?",\
			"What else can I help you with?",\
			"Can I help you with anything else?",\
			"What else can I do for you?",\
			"How else can I be of service?.",\
			"Would you like to know anything else?"]
		return random.choice(questions)

	def weather(self) -> str:
		settings = self.get_settings()
		home_address = settings["homeAddress"]
		lat, lng = geolocation.get_location_from_address(home_address)
		return get_weather(lat, lng)

	def news_title(self) -> str:
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
		return f"{random.choice(intros)} {get_news_title()}. {random.choice(outros)}"
	
	def news_conversation(self, input: str) -> tuple[str, Callable]:
		if any(trigger in input for trigger in AFFIRM_TRIGGERS):
			return f"{get_news_content()} {self.repeat_question()}", self.conversation
		
		return f"Okay. {self.repeat_question()}", self.conversation

	def get_settings(self) -> object:
		return self.settings.get_setting_by_name("goodMorning")
