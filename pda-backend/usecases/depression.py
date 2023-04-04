from usecases.usecase import UseCase
from scheduler import Scheduler
from datetime import datetime, timedelta
from settings_manager import SettingsManager
from kink import inject
import services.jokes 
import services.email_service as email_service

EMAIL_TRIGGER = ["sad", "depressed", "anxious", "lonely", "empty", "worthless", "hopeless", "suicidal"]
JOKE_TRIGGERS = ["homework", "exam", "boring", "bored", "joke"]

@inject
class DepressionUseCase(UseCase):
	def __init__(self, scheduler: Scheduler, settings: SettingsManager):
		self.scheduler = scheduler
		# self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(seconds=10))
		self.settings = settings

	def get_triggerwords(self) -> list[str]:
		return EMAIL_TRIGGER + JOKE_TRIGGERS

	def trigger(self) -> str:
		
		print("Periodic trigger of the example usecase")
		self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(seconds=60))

		# hier kommt der text der an den user gelesen wird hin
		return 

	async def asked(self, input: str) -> str:
		"""
		:param input: the input of the user
		:return: the answer of the usecase
	    """
		if any(trigger in input for trigger in EMAIL_TRIGGER):
			email_service.send_email()
			return "I am sorry to hear that. I will send you an email to get someone to cheer you up."
		elif any(trigger in input for trigger in JOKE_TRIGGERS):
			return await services.jokes.print_joke()
		

	def get_settings(self) -> object:
		"""
		
	"""
		return self.settings.get_setting_by_name("example")
