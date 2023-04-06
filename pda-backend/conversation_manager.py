from typing import Callable

class ConversationManager:
	next_usecase = None

	def has_next_method(self) -> bool:
		return self.next_usecase is not None

	def set_net_method(self, method: Callable | None):
		print(f"Setting next usecase method to {method}")
		self.next_usecase = method

	def get_next_method(self) -> Callable | None:
		return self.next_usecase
