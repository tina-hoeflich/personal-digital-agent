from flask import request, Blueprint, current_app as app
from flask_socketio import SocketIO
from kink import di
from proaktiv_sender import ProaktivSender

trigger_blueprint = Blueprint('trigger_api', __name__, template_folder='templates')
@trigger_blueprint.route('/trigger', methods=['GET'])
def text_input():
	proaktiv: ProaktivSender = di[ProaktivSender]

	proaktiv.send_text("Hallo, ich bin Jarvis!")
	return ('', 204)
