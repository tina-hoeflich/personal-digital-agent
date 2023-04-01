from usecases.usecase import UseCase
import services.tankerkoenig as tankerkoenig
import services.stocks as stocks_service
from scheduler import Scheduler
from settings_manager import SettingsManager
import services.geolocation as geolocation
from kink import inject
from datetime import datetime, timedelta
from proaktiv_sender import ProaktivSender

GENERAL_TRIGGERS = ["save", "money", "cheap", "cheaply"]
FUEL_TRIGGERS = ["fuel", "gas", "car", "fuel", "petrol", "diesel", "e5", "e10"]
STOCK_TRIGGERS = ["stock", "share", "shares", "stock", "stocks", "stockmarket", "stockmarket", "stockexchange"]


@inject
class SparenUseCase(UseCase):
	def __init__(self, scheduler: Scheduler, settings: SettingsManager, proaktive: ProaktivSender):
		self.scheduler = scheduler
		self.settings = settings
		self.proaktive = proaktive
		self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(minutes=10))

	def get_triggerwords(self) -> list[str]:
		return GENERAL_TRIGGERS + FUEL_TRIGGERS + STOCK_TRIGGERS

	def trigger(self) -> str:
		self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(minutes=10))

		text = ""

		text += self.get_stockprice_text(False)
		text += self.get_fuelprice_text(False)

		if text != "":
			text = "Hey! I have some tips for saving some money for you! " + text
			text = self.proaktive.send_text(text)

	def asked(self, input: str) -> str:
		return self.get_fuelprice_text(True) + self.get_stockprice_text(True)

	def get_settings(self) -> object:
		return self.settings.get_setting_by_name("sparen")

	def get_fuelprice_text(self, always: bool) -> str:
		settings = self.get_settings()["sprit"]

		home_address = self.settings.get_setting_by_name("goodMorning")["homeAddress"]
		lat, lng = geolocation.get_location_from_address(home_address)

		location, price = tankerkoenig.get_fuelprice(settings["typ"], lat, lng, settings["radius"])
		if always or price < settings["limit"]:
			text = "The currently lowest {} fuel price is {:.3f}€ at {}.".format(settings["typ"], price, location)

			if price < settings["limit"]:
				text += " This is below your set limit of {:.3f}€. You should go there and fill up!".format(settings["limit"])
			else:
				text += " This is above your set limit of {:.3f}€. Maybe you should wait fueling your car until it is cheaper!".format(settings["limit"])

		return text

	def get_stockprice_text(self, always: bool) -> str:
		"""Get the text for the stock prices

		Args:
			always (bool): Whether to always return the text or only if the price is outside the limits

		Returns:
			str: the text to say
		"""
		favorites = self.get_settings()["stocks"]["favorites"]
		text = ""
		for favorite in favorites:
			outside_limits, price = self.get_string_buy_stock(favorite["symbol"], favorite["priceHigh"], favorite["priceLow"])
			if always or outside_limits:
				text += price + "\n"

		return text

	def get_string_buy_stock(self, stock: str, top_limit: float, bottom_limit: float) -> tuple[bool, str]:
		"""Get the text for one stock price

		Args:
			stock (str): the stock ticker symbol
			top_limit (float): the top limit
			bottom_limit (float): the bottom limit

		Returns:
			tuple[bool, str]: whether the price is outside the limits and the text to say
		"""
		price = stocks_service.get_stock_price(stock)
		if price > top_limit:
			return True, "The stock price of {} is {:.2f}€. This is above your set limit of {:.2f}€. This is looking great! You will be rich soon!".format(stock, price, top_limit)
		if price < bottom_limit:
			return True, "The stock price of {} is {:.2f}€. This is below your set limit of {:.2f}€. Maybe you should sell all your stocks now!".format(stock, price, bottom_limit)
		return False, "The stock price of {} is {:.2f}€. This is not above or below your limits".format(stock, price)
