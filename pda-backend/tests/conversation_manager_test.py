from conversation_manager import ConversationManager


def test_no_conversation():
	conv_manager = ConversationManager()
	conv_manager.set_net_method(None)

	assert not conv_manager.has_next_method()


def test_has_conversation():
	conv_manager = ConversationManager()
	def test_callable(x): return True
	conv_manager.set_net_method(test_callable)
	next = conv_manager.get_next_method()
	assert id(test_callable) == id(next)

	assert conv_manager.has_next_method()
