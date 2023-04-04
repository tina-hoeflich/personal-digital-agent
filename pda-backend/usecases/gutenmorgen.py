from usecases.usecase import UseCase
from scheduler import Scheduler
from services.weather import get_weather
import services.geolocation as geolocation
from settings_manager import SettingsManager
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

	def trigger(self) -> str:
	# hier kommt das periodische checken für proaktive Dinge rein.

	# hier muss jeder trigger noch den nächsten run schedulen. Aktuell geht das nicht, wir haben ja noch keinen scheduler.

	# hier kommt der text der an den user gelesen wird hin
		return "Periodic trigger of the example usecase"

	async def asked(self, input: str) -> str:
		return f"{self.greeting()} {self.weather()}"
	
	def greeting(self) -> str:
		name = self.get_settings()["name"]
		greetings = [
			f"Good Morning {name}, let's get your day started!",\
			f"Welcome back {name}, how may i help you today?",\
			f"Good Morning {name}, let me know how I can assist you today.",\
			f"Good Morning {name}, another day, another opportunity to assist you.",\
			f"Welcome back {name}. Let me know if I can be of service.",\
			f"Rise and shine {name}! I'm here and ready to help."]
		return random.choice(greetings)

	def weather(self) -> str:
		settings = self.get_settings()
		home_address = settings["homeAddress"]
		lat, lng = geolocation.get_location_from_address(home_address)
		return get_weather(lat, lng)

	def get_settings(self) -> object:
		return self.settings.get_setting_by_name("goodMorning")
