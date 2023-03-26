from usecases.example import ExampleUseCase
from usecases.usecase import UseCase
from __main__ import app
from flask import request
import json

@app.route('/setPreferences', methods=['POST'])
def set_preferences():
    settings_json = request.get_data(as_text=True)
    # convert json string to dictionary
    settings_dict = json.loads(settings_json)
    # create new json output file from dictionary
    settings_json_obj = json.dumps(settings_dict, indent=4)
    # write json object to file
    with open("api/user/userSettings.json", "w") as settings_file:
        settings_file.write(settings_json_obj)
    
    response = "Accepted"
    return response