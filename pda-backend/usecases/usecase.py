from abc import ABC, abstractmethod
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
	def asked(self, input: str) -> str:
		"""Method getting called when the user mentioned one of the triggerwords

		Args:
			input (str): full text input from the user

		Returns:
			str: text to read back to the user
		"""
		pass

	@abstractmethod
	def get_settings() -> object:
		"""Get the settings of the usecase

		Returns:
			dict: settings
		"""
		return None
