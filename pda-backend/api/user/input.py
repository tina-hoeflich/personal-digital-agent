from conversation_manager import ConversationManager
from usecases.example import ExampleUseCase
from usecases.usecase import UseCase
from usecases.sparsupport import SparenUseCase
from usecases.depression import DepressionUseCase
from usecases.gutenmorgen import GutenMorgenUseCase
from flask import request, Blueprint, current_app as app
from kink import di
import inspect
import random

USECASES: list[UseCase] = [ExampleUseCase(), SparenUseCase(), DepressionUseCase(), GutenMorgenUseCase()]

input_blueprint = Blueprint('input_api', __name__, template_folder='templates')


@input_blueprint.route('/input', methods=['POST'])
async def text_input():
	message = request.get_data(as_text=True)
	app.logger.info("Nachricht empfangen: {}".format(message))

	conversation_manager: ConversationManager = di[ConversationManager]

	selected_usecase = None

	if not conversation_manager.has_next_method():
		# no next usecase from conversation
		for usecase in USECASES:
			triggers = usecase.get_triggerwords()
			if any(trigger in message for trigger in triggers):
				selected_usecase = usecase
				break

		response = None
		if selected_usecase is None:
			response = random.choice(["I didn't understand you. Please try again"])
		else:
			app.logger.info("Using UseCase handler {}".format(selected_usecase))
			response, new_usecase = await selected_usecase.asked(message)
	else:
		next_method = conversation_manager.get_next_method()
		app.logger.info(f"Found next method from conversation history. Using method {next_method}")
		if inspect.iscoroutine(next_method):
			response, new_usecase = await next_method(message)
		else:
			response, new_usecase = next_method(message)

	conversation_manager.set_net_method(new_usecase)

	app.logger.info("Responding with: {}".format(response))
	return response
