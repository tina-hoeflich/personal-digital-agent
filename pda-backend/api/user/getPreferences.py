from usecases.example import ExampleUseCase
from usecases.usecase import UseCase
from __main__ import app
from flask import request

@app.route('/getPreferences', methods=['GET'])
def get_preferences():
    pass