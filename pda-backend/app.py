from flask import Flask
from flask_cors import CORS

from conversation_manager import ConversationManager
from settings_manager import SettingsManager
from scheduler import Scheduler
from kink import di
from flask_socketio import SocketIO
from proaktiv_sender import ProaktivSender

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')

# Dependency injection setup
set_man = SettingsManager('settings.json')
sched = Scheduler()
proaktiv = ProaktivSender(socketio)
conv_man = ConversationManager()

# Core services
di[SettingsManager] = set_man
di[Scheduler] = sched
di[ProaktivSender] = proaktiv
di[ConversationManager] = conv_man


# das sagt, dass die api routes aus api/user/input.py und api/user/settings.py geladen werden sollen
from api.user.input import input_blueprint
from api.user.settings import settings_blueprint
from api.developer.trigger import trigger_blueprint
app.register_blueprint(input_blueprint)
app.register_blueprint(settings_blueprint)
app.register_blueprint(trigger_blueprint)

if __name__ == "__main__":  # pragma: no cover
	socketio.run(app, host="0.0.0.0", port=8000)
