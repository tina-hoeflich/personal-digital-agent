from usecases.usecase import UseCase
from scheduler import Scheduler
from services.weather import get_weather
import services.geolocation as geolocation
from settings_manager import SettingsManager
from typing import Callable
import random
from kink import inject

GENERAL_TRIGGERS = ["morning", "day", "rise", "alarm"]
HELP_TRIGGERS = ["help", "know", "how"]
WEATHER_TRIGGERS = ["weather", "temperature", "warm", "cold", "rain", "rainy", "sunny", "sun", "cloud", "clouds", "cloudy"]

CANCEL_TRIGGERS = ["no", "nothing", "bye", "leave", "stop", "usecase"]

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
			return "Good bye!", None
		if any(trigger in input for trigger in HELP_TRIGGERS):
			return "I can tell you about the weather, or you can try another usecase by saying bye!", self.conversation
		if any(trigger in input for trigger in WEATHER_TRIGGERS):
			return self.weather() + " " + self.repeat_question(), self.conversation 
		
		return "I didn't understand you, please try again", self.conversation

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
			"How can I be of service tody?.",\
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

	def get_settings(self) -> object:
		return self.settings.get_setting_by_name("goodMorning")
