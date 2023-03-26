from usecases.example import ExampleUseCase
from usecases.usecase import UseCase
from __main__ import app
from flask import request
import json

@app.route('/getPreferences', methods=['GET'])
def get_preferences():
    settings_file = open("api/user/userSettings.json")
    response = settings_file.read()
    # print(response)
    return response