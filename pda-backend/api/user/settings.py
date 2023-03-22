from __main__ import app
from flask import request
import settings_manager

@app.route('/settings', methods=['GET'])
def get_settings():
	return settings_manager.get_all_settings()

@app.route('/settings', methods=['POST'])
def set_settings():
	body = request.get_json()
	return settings_manager.set_settings(body)
