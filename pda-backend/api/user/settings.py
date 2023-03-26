from flask import request, Blueprint
import settings_manager

settings_blueprint = Blueprint('settings_api', __name__, template_folder='templates')
@settings_blueprint.route('/settings', methods=['GET'])
def get_settings():
	return settings_manager.get_all_settings()

@settings_blueprint.route('/settings', methods=['POST'])
def set_settings():
	body = request.get_json()
	return settings_manager.set_settings(body)
