from usecases.usecase import UseCase
from scheduler import Scheduler
from datetime import datetime, timedelta
from settings_manager import SettingsManager
from kink import inject

@inject
class ExampleUseCase(UseCase):
	def __init__(self, scheduler: Scheduler, settings: SettingsManager):
		self.scheduler = scheduler
		# self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(seconds=10))
		self.settings = settings

	def get_triggerwords(self) -> list[str]:
		return ["example"]

	def trigger(self) -> str:
		# hier kommt das periodische checken für proaktive Dinge rein.

		# hier muss jeder trigger noch den nächsten run schedulen. Aktuell geht das nicht, wir haben ja noch keinen scheduler.

		print("Periodic trigger of the example usecase")
		self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(seconds=60))

		# hier kommt der text der an den user gelesen wird hin
		return ""

	def asked(self, input: str) -> str:
		name = self.settings.get_setting_by_name("example")["name"]
		return f"{name} said: " + input

	def get_settings() -> object:
		return self.settings.get_setting_by_name("example")
