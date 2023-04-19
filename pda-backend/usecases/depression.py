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
JOKE_TRIGGERS = ["homework", "boring", "bored", "joke"]
MUSIC_TRIGGERS = ["music", "song", "playlist", "spotify", "exam"]
@inject
class DepressionUseCase(UseCase):
	def __init__(self, scheduler: Scheduler, settings: SettingsManager):
		self.scheduler = scheduler
		# self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(seconds=10))
		self.settings = settings

	def get_triggerwords(self) -> list[str]:
		"""
		:return: the triggerwords of the usecase
		"""
		return EMAIL_TRIGGER + JOKE_TRIGGERS + MUSIC_TRIGGERS

	def trigger(self):
		"""
		Trigger method that is called periodically
		"""
		print("Periodic trigger of the example usecase")
		self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(seconds=60))

	async def asked(self, input: str) -> tuple[str, Callable]:
		"""
		:param input: the input of the user
		:return: the answer of the usecase
	    """
		if any(trigger in input for trigger in EMAIL_TRIGGER):

			return "Should I get someone to cheer you up?", self.emailConversation
		elif any(trigger in input for trigger in JOKE_TRIGGERS):
			return await services.jokes.get_joke(), None
		elif any(trigger in input for trigger in MUSIC_TRIGGERS):

			return "Should I play some music, to brighten up your day", self.musicConversation

	def emailConversation(self, input: str) -> tuple[str, Callable]:
		"""
		Method that listens for the user input and sends an email if the user says yes
		:param input: the input of the user
		"""
		if "yes" in input:
			email_service.send_email("jarvis@tinahoeflich.de",
									 self.get_settings()["emergencyEmail"],
									 "Jarvis asking for your support",
									 "Hi there, \n \nyour friend Tina may need someone to cheer him up :) \nCan you help me out with this? \n \nThanks, \n Jarvis")
			return "I am sorry to hear that. I will send an email to get someone to cheer you up.", None

	def musicConversation(self, input: str) -> tuple[str, Callable]:
		"""
		param input: the input of the user
		Method that listens for the user input and starts music if the user says yes
		"""
		if "yes" in input:
			spotify_service.start_music()
			return "Okay, music started ", self.musicConversation2
		else:
			return "Okay, Can I do anything else for you? ", None

	def musicConversation2(self, input: str) -> tuple[str, Callable]:
		"""
		param input: the input of the user
		Method that listens for the user input and stops music if the user says yes
		"""
		if "stop" in input:
			spotify_service.stop_music()
			return "Music stopped ", None
		else:
			return "Okay, Can I do anything else for you? ", None

	def get_settings(self) -> object:
		"""
		Method that returns the settings of the usecase
		:return: the settings of the usecase
	"""
		return self.settings.get_setting_by_name("depressionHandler")
