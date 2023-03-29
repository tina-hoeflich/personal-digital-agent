from usecases.usecase import UseCase
from scheduler import Scheduler
from datetime import datetime, timedelta
from settings_manager import SettingsManager
from kink import inject
import services.jokes 

@inject
class DepressionUseCase(UseCase):
	def __init__(self, scheduler: Scheduler, settings: SettingsManager):
		self.scheduler = scheduler
		# self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(seconds=10))
		self.settings = settings

	def get_triggerwords(self) -> list[str]:
		return ["joke", "sad"]

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
		return await services.jokes.print_joke()

	def get_settings(self) -> object:
		"""
		
	"""
		return self.settings.get_setting_by_name("example")
