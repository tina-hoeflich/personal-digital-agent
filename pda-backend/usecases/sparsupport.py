from typing import Callable

from conversation_manager import ConversationManager
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
STOCK_TRIGGERS = ["stock", "share", "shares", "stock", "stocks", "stockmarket", "stockmarket"]


@inject
class SparenUseCase(UseCase):
	talk_fuelprice = False
	talk_stockprice = False

	def __init__(self, scheduler: Scheduler, settings: SettingsManager, proaktive: ProaktivSender, conv_man: ConversationManager):
		self.scheduler = scheduler
		self.settings = settings
		self.proaktive = proaktive
		self.conv_man = conv_man
		self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(minutes=4))

	def get_triggerwords(self) -> list[str]:
		return GENERAL_TRIGGERS + FUEL_TRIGGERS + STOCK_TRIGGERS

	def trigger(self):
		self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(minutes=4))

		_, talk_fuelprice, talk_stockprice = self.get_general_text()
		self.talk_stockprice = talk_stockprice
		self.talk_fuelprice = talk_fuelprice

		if self.talk_fuelprice or self.talk_stockprice:
			text = "Hey! I have some tips for saving some money for you! Do you want to hear them?"
			self.proaktive.send_text(text)
			self.conv_man.set_net_method(self.conversation)

	async def asked(self, input: str) -> tuple[str, Callable | None]:
		text, talk_fuelprice, talk_stockprice = self.get_general_text()
		self.talk_stockprice = talk_stockprice
		self.talk_fuelprice = talk_fuelprice
		if self.talk_fuelprice or self.talk_stockprice:
			return text, self.conversation, None, None
		return text, None, None, None

	def conversation(self, input: str) -> tuple[str, Callable | None]:
		if " no " in " " + input.lower() + " ":
			return "Can I do something else for you?", None, None, None

		text = ""
		if self.talk_fuelprice:
			text += self.get_fuelprice_text(False)
		if self.talk_stockprice:
			text += self.get_stockprice_text(False)
		return text, None, None, None

	def get_settings(self) -> object:
		return self.settings.get_setting_by_name("sparen")

	def get_general_text(self) -> tuple[str, bool, bool]:
		_, fuelprice = self.get_fuelprice()
		fuel_good = fuelprice < self.get_settings()["sprit"]["preisschwelle"]
		stock_good = self.get_stock_yes_no()

		text = ""
		if fuel_good:
			text += "I have news for saving money at the gas station. Do you want to hear it? \n"
		if stock_good:
			text += "I have news for gaining some fast money at the stock market. Do you want to hear it?"
		return text, fuel_good, stock_good, None, None

	def get_fuelprice(self) -> tuple[str, float]:
		settings = self.get_settings()["sprit"]

		home_address = self.settings.get_setting_by_name("goodMorning")["homeAddress"]
		lat, lng = geolocation.get_location_from_address(home_address)

		return tankerkoenig.get_fuelprice(settings["typ"], lat, lng, settings["radius"])

	def get_fuelprice_text(self, always: bool) -> str:
		settings = self.get_settings()["sprit"]

		location, price = self.get_fuelprice()
		if always or price < settings["preisschwelle"]:
			text = "The currently lowest {} fuel price is {:.3f}€ at {}.".format(settings["typ"], price, location)

			if price < settings["preisschwelle"]:
				text += " This is below your set limit of {:.3f}€. You should go there and fill up!".format(settings["preisschwelle"])
			else:
				text += " This is above your set limit of {:.3f}€. Maybe you should wait fueling your car until it is cheaper!".format(settings["preisschwelle"])

		return text

	def get_stock_yes_no(self) -> bool:
		good = False
		for stock in self.get_settings()["stocks"]["favorites"]:
			price = stocks_service.get_stock_price(stock["symbol"])
			if price > stock["priceHigh"] or price < stock["priceLow"]:
				good = True
				break

		return good

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
