from usecases.usecase import UseCase
from services.tankerkoenig import get_fuelprice
from services.stocks import get_stock_price
from scheduler import Scheduler
from settings_manager import SettingsManager
from kink import inject
from datetime import datetime, timedelta

GENERAL_TRIGGERS = ["save", "money", "cheap", "cheaply"]
FUEL_TRIGGERS = ["fuel", "gas", "car", "fuel", "petrol", "diesel", "e5", "e10"]
STOCK_TRIGGERS = ["stock", "share", "shares", "stock", "stocks", "stockmarket", "stockmarket", "stockexchange"]

@inject
class SparenUseCase(UseCase):
	def __init__(self, scheduler: Scheduler, settings: SettingsManager):
		self.scheduler = scheduler
		self.settings = settings
		self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(minutes=10))

	def get_triggerwords(self) -> list[str]:
		return GENERAL_TRIGGERS + FUEL_TRIGGERS + STOCK_TRIGGERS

	def trigger(self) -> str:
		self.scheduler.schedule_job(trigger, datetime.now() + timedelta(minutes=10))
		# hier kommt das periodische checken für proaktive Dinge rein.

		# hier muss jeder trigger noch den nächsten run schedulen. Aktuell geht das nicht, wir haben ja noch keinen scheduler.

		# hier kommt der text der an den user gelesen wird hin
		return "Periodic trigger of the example usecase"

	def asked(self, input: str) -> str:
		return self.get_fuelprice_text() + self.get_stockprice_text(True)

	def get_fuelprice_text(self) -> str:
		settings = self.get_settings()["sprit"]
		location, price = get_fuelprice(settings["typ"], settings["lat"], settings["lng"], settings["radius"])
		text = "The currently lowest {} fuel price is {:.3f}€ at {}.".format(settings["typ"], price, location)
		if price < settings["limit"]:
			text += " This is below your set limit of {:.3f}€. You should go there and fill up!".format(settings["limit"])
		else:
			text += " This is above your set limit of {:.3f}€. Maybe you should wait fueling your car until it is cheaper!".format(settings["limit"])
		return text

	def get_settings(self) -> object:
		return self.settings.get_setting_by_name("sparen")

	def get_stockprice_text(self, all: bool) -> str:
		favorites = self.get_settings()["stocks"]["favorites"]
		text = ""
		for favorite in favorites:
			talk, price = self.get_string_buy_stock(favorite["symbol"], favorite["priceHigh"], favorite["priceLow"])
			if all or talk:
				text += price + "\n"

		return text

	def get_string_buy_stock(self, stock: str, top_limit: float, bottom_limit: float) -> tuple[bool, str]:
		price = get_stock_price(stock)
		if price > top_limit:
			return True, "The stock price of {} is {:.2f}€. This is above your set limit of {:.2f}€. This is looking great! You will be rich soon!".format(stock, price, top_limit)
		if price < bottom_limit:
			return True, "The stock price of {} is {:.2f}€. This is below your set limit of {:.2f}€. Maybe you should sell all stocks now!".format(stock, price, bottom_limit)
		return False, "The stock price of {} is {:.2f}€. This is not above or below your limits".format(stock, price)
