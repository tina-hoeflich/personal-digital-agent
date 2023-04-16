from abc import ABC, abstractmethod
from typing import Callable


class UseCase(ABC):   # pragma: no cover

	@abstractmethod
	def get_triggerwords(self) -> list[str]:
		"""Get the triggerwords triggering the usecase when asked by the user

		Returns:
			List[str]: list of triggerwords
		"""
		pass

	@abstractmethod
	def trigger(self):
		"""This method gets called by the scheduler when the next scheduled time is hit
		"""
		pass

	@abstractmethod
	def asked(self, input: str) -> tuple[str, Callable, str, str]:
		"""Method getting called when the user mentioned one of the triggerwords

		Args:
			input (str): full text input from the user

		Returns:
			str: text to read back to the user
			Callable: the method to call for the next user input. This manages the conversation logic
			str: the link of the image url
			str: the link url for a webpage
		"""
		pass

	@abstractmethod
	def get_settings(self) -> object:
		"""Get the settings of the usecase

		Returns:
			dict: settings
		"""
		return None
