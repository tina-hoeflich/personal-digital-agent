from usecases.example import ExampleUseCase
from usecases.usecase import UseCase
from __main__ import app
from flask import request
import random

@app.route('/input', methods=['POST'])
def text_input():
    message = request.get_data(as_text=True)
    app.logger.info("Nachricht empfangen: {}".format(message))

    usecases: List[UseCase] = [ExampleUseCase()]
    selected_usecase = None

    for usecase in usecases:
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
