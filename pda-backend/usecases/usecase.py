from abc import ABC, abstractmethod
from typing import Callable
import types

class UseCase(ABC):

	@abstractmethod
	def get_triggerwords(self) -> list[str]:
		"""Get the triggerwords triggering the usecase when asked by the user

		Returns:
			List[str]: list of triggerwords
		"""
		pass

	@abstractmethod
	def trigger(self) -> str:
		"""This method gets called by the scheduler when

		Returns:
			str: output text read to the user
		"""
		pass

	@abstractmethod
	def asked(self, input: str) -> tuple[str, Callable]:
		"""Method getting called when the user mentioned one of the triggerwords

		Args:
			input (str): full text input from the user

		Returns:
			str: text to read back to the user
			Callable: the method to call for the next user input. This manages the conversation logic
		"""
		pass

	@abstractmethod
	def get_settings() -> object:
		"""Get the settings of the usecase

		Returns:
			dict: settings
		"""
		return None
