from usecases.usecase import UseCase
from scheduler import Scheduler
from services.weather import get_weather
import services.geolocation as geolocation
from settings_manager import SettingsManager
from typing import Callable
import random
from kink import inject

TRIGGERS = ["morning", "day", "weather", "traffic", "alarm"]

@inject
class GutenMorgenUseCase(UseCase):
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
		return f"{self.greeting()} {self.weather()}", None

	def greeting(self) -> str:
		name = self.get_settings()["name"]
		greetings = [
			f"Good Morning {name}, let's get your day started! What would you like to do?",\
			f"Welcome back {name}, how may i help you today?",\
			f"Good Morning {name}, let me know how I can assist you today.",\
			f"Good Morning {name}. Let me know what I can do for you.",\
			f"Welcome back {name}. Let me know how I can be of service.",\
			f"Rise and shine {name}! I'm here and ready to help. What would you like to know about?"]
		return random.choice(greetings)
	
	def conversation(self) -> str:
		text = ""
		return text, None

	def weather(self) -> str:
		settings = self.get_settings()
		home_address = settings["homeAddress"]
		lat, lng = geolocation.get_location_from_address(home_address)
		return get_weather(lat, lng)

	def get_settings(self) -> object:
		return self.settings.get_setting_by_name("goodMorning")
