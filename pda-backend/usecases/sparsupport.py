from usecases.usecase import UseCase
from services.tankerkoenig import get_fuelprice
from services.stocks import get_stock_price
from scheduler import Scheduler
from settings_manager import SettingsManager
from kink import inject

GENERAL_TRIGGERS = ["save", "money", "cheap", "cheaply"]
FUEL_TRIGGERS = ["fuel", "gas", "car", "fuel", "petrol", "diesel", "e5", "e10"]
STOCK_TRIGGERS = ["stock", "share", "shares", "stock", "stocks", "stockmarket", "stockmarket", "stockexchange"]

@inject
class SparenUseCase(UseCase):
	def __init__(self, scheduler: Scheduler, settings: SettingsManager):
		self.scheduler = scheduler
		self.settings = settings

	def get_triggerwords(self) -> list[str]:
		return GENERAL_TRIGGERS + FUEL_TRIGGERS + STOCK_TRIGGERS

	def trigger(self) -> str:
		# hier kommt das periodische checken für proaktive Dinge rein.

		# hier muss jeder trigger noch den nächsten run schedulen. Aktuell geht das nicht, wir haben ja noch keinen scheduler.

		# hier kommt der text der an den user gelesen wird hin
		return "Periodic trigger of the example usecase"

	def asked(self, input: str) -> str:
		if any(trigger in input for trigger in FUEL_TRIGGERS):
			return self.current_fuelprice()
		if any(trigger in input for trigger in STOCK_TRIGGERS):
			return self.current_stockprice()

	def current_fuelprice(self) -> str:
		settings = self.get_settings()["sprit"]
		location, price = get_fuelprice(settings["typ"], settings["lat"], settings["lng"], settings["radius"])
		return "The currently lowest {} fuel price is {:.3f}€ at {}.".format(settings["typ"], price, location)

	def current_stockprice(self) -> str:
		symbol = "P911.DEX"
		price = get_stock_price(symbol)
		return "The stock price of {} is {:.2f}€.".format(symbol, price)

	def get_settings(self) -> object:
		return self.settings.get_setting_by_name("sparen")
