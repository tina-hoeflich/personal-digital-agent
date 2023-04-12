from usecases.usecase import UseCase
from scheduler import Scheduler
from datetime import datetime, timedelta
from settings_manager import SettingsManager
from kink import inject
from typing import Callable
import services.jokes
import services.email_service as email_service
import services.spotify_service as spotify_service

EMAIL_TRIGGER = ["sad", "depressed", "anxious", "lonely", "empty", "worthless", "hopeless", "suicidal"]
JOKE_TRIGGERS = ["homework", "exam", "boring", "bored", "joke"]
MUSIC_TRIGGERS = ["music", "song", "playlist", "spotify"]
@inject
class DepressionUseCase(UseCase):
	def __init__(self, scheduler: Scheduler, settings: SettingsManager):
		self.scheduler = scheduler
		# self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(seconds=10))
		self.settings = settings

	def get_triggerwords(self) -> list[str]:
		return EMAIL_TRIGGER + JOKE_TRIGGERS + MUSIC_TRIGGERS

	def trigger(self):

		print("Periodic trigger of the example usecase")
		self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(seconds=60))

	async def asked(self, input: str) -> tuple[str, Callable]:
		"""
		:param input: the input of the user
		:return: the answer of the usecase
	    """
		if any(trigger in input for trigger in EMAIL_TRIGGER):
			email_service.send_email("jarvis@tinahoeflich.com",
									 self.get_settings()["emergencyEmail"],
									 "Jarvis asking for your support",
									 "Hi there, \n \nyour friend may need someone to cheer him up :) \nCan you help me out with this? \n \nThanks, \n Jarvis")
			return "I am sorry to hear that. I will send an email to get someone to cheer you up.", None
		elif any(trigger in input for trigger in JOKE_TRIGGERS):
			return await services.jokes.get_joke(), None
		elif any(trigger in input for trigger in MUSIC_TRIGGERS):
			spotify_service.start_music()
			return "Let me play some music, to brighten up your day", None


	def get_settings(self) -> object:
		"""

	"""
		return self.settings.get_setting_by_name("depressionHandler")
