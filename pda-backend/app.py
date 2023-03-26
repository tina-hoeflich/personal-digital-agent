from flask import Flask, request
from flask_cors import CORS
from settings_manager import SettingsManager
from scheduler import Scheduler
from kink import di

app = Flask(__name__)
CORS(app)

# Dependency injection setup
set_man = SettingsManager('settings.json')
sched = Scheduler()

# Core services
di[SettingsManager] = set_man
di[Scheduler] = sched

# das sagt, dass die api routes aus api/user/input.py und api/user/settings.py geladen werden sollen
from api.user.input import input_blueprint
from api.user.settings import settings_blueprint
app.register_blueprint(input_blueprint)
app.register_blueprint(settings_blueprint)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)
