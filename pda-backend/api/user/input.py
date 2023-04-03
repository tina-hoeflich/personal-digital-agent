from usecases.example import ExampleUseCase
from usecases.usecase import UseCase
from usecases.sparsupport import SparenUseCase
from usecases.gutenmorgen import GutenMorgenUseCase
from flask import request, Blueprint, current_app as app
import random

USECASES: list[UseCase] = [ExampleUseCase(), SparenUseCase(), GutenMorgenUseCase()]

input_blueprint = Blueprint('input_api', __name__, template_folder='templates')
@input_blueprint.route('/input', methods=['POST'])
def text_input():
    message = request.get_data(as_text=True)
    app.logger.info("Nachricht empfangen: {}".format(message))

    selected_usecase = None

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
        response = selected_usecase.asked(message)

    app.logger.info("Responding with: {}".format(response))
    return response
