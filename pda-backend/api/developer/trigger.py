from flask import Blueprint
from kink import di

import api.user.input
from proaktiv_sender import ProaktivSender
from usecases.gutenmorgen import GutenMorgenUseCase
from usecases.sparsupport import SparenUseCase
from usecases.netflix_and_chill import NetflixAndChillUseCase

trigger_blueprint = Blueprint('trigger_api', __name__, template_folder='templates')
@trigger_blueprint.route('/trigger', methods=['GET'])
def text_input(): #pragma: no cover
	proaktiv: ProaktivSender = di[ProaktivSender]

	proaktiv.send_text("Hallo, ich bin Jarvis!")
	return ('', 204)

@trigger_blueprint.route('/trigger/guten_morgen', methods=['GET'])
def trigger_guten_morgen(): #pragma: no cover
	arr = api.user.input.USECASES
	gumo_usecase = [uc for uc in arr if isinstance(uc, GutenMorgenUseCase)][0]
	gumo_usecase.trigger()
	return ('', 204)

@trigger_blueprint.route('/trigger/sparsupport', methods=['GET'])
def trigger_sparsupport(): #pragma: no cover
	arr = api.user.input.USECASES
	sparen_usecase = [uc for uc in arr if isinstance(uc, SparenUseCase)][0]
	sparen_usecase.trigger()
	return ('', 204)

@trigger_blueprint.route('/trigger/netflix', methods=['GET'])
def trigger_netflix(): #pragma: no cover
	arr = api.user.input.USECASES
	netflix_usecase = [uc for uc in arr if isinstance(uc, NetflixAndChillUseCase)][0]
	netflix_usecase.trigger()
	return ('', 204)
