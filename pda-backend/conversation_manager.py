from typing import Callable


class ConversationManager:
	next_usecase = None

	def has_next_method(self) -> bool:
		return self.next_usecase is not None

	def set_net_method(self, method: Callable):
		self.next_usecase = method

	def get_next_method(self) -> Callable:
		return self.next_usecase
