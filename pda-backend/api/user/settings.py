from flask import request, Blueprint
from flask_cors import CORS
from settings_manager import SettingsManager

set_man = SettingsManager('settings.json')

settings_blueprint = Blueprint('settings_api', __name__, template_folder='templates')
@settings_blueprint.route('/settings', methods=['GET'])
def get_settings():
	return set_man.get_all_settings()

@settings_blueprint.route('/settings', methods=['POST'])
def set_settings():
	body = request.get_json()
	return set_man.save_settings(body)
