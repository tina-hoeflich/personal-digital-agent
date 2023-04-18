from cachetools import cached, TTLCache
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
import random

GENERAL_TRIGGERS = ["save", "money", "cheap", "cheaply"]
FUEL_TRIGGERS = ["fuel", "gas", "car", "fuel", "petrol", "diesel", "e5", "e10"]
STOCK_TRIGGERS = ["stock", "share", "shares", "stock", "stocks", "stockmarket", "stockmarket"]

CANCEL_TRIGGERS = ["no", "nothing", "bye", "stop", "usecase", "never"]
AFFIRM_TRIGGERS = ["yes", "sure", "okay", "ok", "fine", "gladly"]

stockprice_cache = TTLCache(maxsize=10, ttl=120)


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
		self.scheduler.schedule_job(self.trigger, datetime.now() + timedelta(minutes=10))

		_, talk_fuelprice, talk_stockprice = self.get_general_text()
		self.talk_stockprice = talk_stockprice
		self.talk_fuelprice = talk_fuelprice

		if self.talk_fuelprice or self.talk_stockprice:
			text_possibilities = ["Hey! I have some tips for saving some money for you! Do you want to hear them?",
								  "Are you here? I have tips for saving money. Wanna hear them?",
								  "Excuse me, do you have a moment? I could share with you some great tips on saving money.",
								  "Hi there! I've got some tips on how to save money that I'd love to share with you. Are you interested?"]
			text = random.choice(text_possibilities)
			self.proaktive.send_text(text)
			self.conv_man.set_net_method(self.conversation)

	async def asked(self, input: str) -> tuple[str, Callable or None]:
		input = input.split(" ")
		if any(trigger in input for trigger in FUEL_TRIGGERS):
			return self.get_fuelprice_text(True), None
		if any(trigger in input for trigger in STOCK_TRIGGERS):
			return self.get_stockprice_text(True), None

		# converstaion only if no specific trigger was mentioned
		text, talk_fuelprice, talk_stockprice = self.get_general_text()
		self.talk_stockprice = talk_stockprice
		self.talk_fuelprice = talk_fuelprice
		if self.talk_fuelprice or self.talk_stockprice:
			return text, self.conversation
		return text, None

	def conversation(self, input: str) -> tuple[str, Callable or None]:
		input = input.split(" ")
		if any(trigger in input for trigger in CANCEL_TRIGGERS):
			text_possibilities = ["Can I do something else for you?",
								  "That's okay. Want anything else.",
								  "No problem. I'm here if you need me."]
			return random.choice(text_possibilities), None

		text = ""
		if self.talk_fuelprice:
			text += self.get_fuelprice_text(any(trigger in input for trigger in FUEL_TRIGGERS)) + " "
		if self.talk_stockprice:
			text += self.get_stockprice_text(any(trigger in input for trigger in STOCK_TRIGGERS))
		return text, None

	def get_settings(self) -> object:
		return self.settings.get_setting_by_name("sparen")

	def get_general_text(self) -> tuple[str, bool, bool]:
		_, fuelprice = self.get_fuelprice()
		fuel_good = fuelprice < self.get_settings()["sprit"]["preisschwelle"]
		stock_good = self.get_stock_yes_no()

		text = ""
		if fuel_good:
			text_possible = ["Good news! I've got some money-saving tips for the gas station that you might want to hear about. Would you like me to share them with you? \n",
							 "I have news for saving money at the gas station. Do you want to hear it? \n",
							 "Sure. There are news about the fule prices. Do you want to hear them?"]
			text += random.choice(text_possible) + "\n"
		if stock_good:
			text_possible = ["I have news for gaining some fast money at the stock market. Do you want to hear it?",
							 "I have information about your favorite stocks. Do you have some time for them?",
							 "Do you want to hear the stock price news I have?"]
			text += random.choice(text_possible)
		return text, fuel_good, stock_good

	def get_fuelprice(self) -> tuple[str, float]:
		settings = self.get_settings()["sprit"]

		home_address = self.settings.get_setting_by_name("goodMorning")["homeAddress"]
		lat, lng = geolocation.get_location_from_address(home_address)

		return tankerkoenig.get_fuelprice(settings["typ"], lat, lng, settings["radius"])

	def get_fuelprice_text(self, always: bool) -> str:
		settings = self.get_settings()["sprit"]

		location, price = self.get_fuelprice()
		text = ""
		if always or price < settings["preisschwelle"]:
			text_possible = ["The currently lowest {} fuel price is {:.3f}€ at {}.".format(settings["typ"], price, location),
							 f"The cheapest {settings['typ']} gas station is at {location} with a price of {price:.3f}€."]
			text = random.choice(text_possible)

			if price < settings["preisschwelle"]:
				text_possible = [f"This is below your set limit of {settings['preisschwelle']:.3f}€.",
								 f"Your limit is {settings['preisschwelle']:.3f}€."]
				text += " " + random.choice(text_possible)
				text_possible = ["You should go there and fill up!",
								 "Go there and bring a canister with you!"]
				text += " " + random.choice(text_possible)
			else:
				text_possible = [f"This is above your set limit of {settings['preisschwelle']:.3f}€.",
								 f"Your limit is {settings['preisschwelle']:.3f}€."]
				text += " " + random.choice(text_possible)
				text_possible = ["Maybe you should wait fueling your car until it is cheaper!",
								 "Use public transport until fuel is cheaper again."]
				text += " " + random.choice(text_possible)

		return text

	def get_stock_yes_no(self) -> bool:
		good = False
		for stock in self.get_settings()["stocks"]["favorites"]:
			price = self.get_stock_price(stock["symbol"])
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
		price = self.get_stock_price(stock)
		text_possible = [f"The stock price of {stock} is {price:.2f}€.",
						 f"The stock '{stock}' is currently trading for a price of {price:.2f}€",
						 f"You can buy or sell '{stock}' for about {price:.2f}€ right now."]
		text = random.choice(text_possible)
		if price > top_limit:
			text_possible = [f"Your limit is {top_limit:.2f}€",
							 f"This is above your set limit of {top_limit:.2f}€"]
			text = text + " " + random.choice(text_possible)
			text_possible = ["Stocks only go up!",
							 "This is looking great! You will be rich soon!"]
			text = text + " " + random.choice(text_possible)
			return True, text
		if price < bottom_limit:
			text_possible = [f"Your limit is {bottom_limit:.2f}€",
							 f"This is below your set limit of {bottom_limit:.2f}€"]
			text = text + " " + random.choice(text_possible)
			text_possible = ["Maybe you should sell all your stocks now!",
							 "Maybe this stock is the next Wirecard stock?"]
			text = text + " " + random.choice(text_possible)
			return True, text
		text_possible = ["This is not above or below your limits.",
						 "Nothing really interesting."]
		return False, text + " " + random.choice(text_possible)

	@cached(stockprice_cache)
	def get_stock_price(self, stock: str) -> float:
		"""
		Get the price of a stock symbol. This function uses a cache
		Args:
			stock: the stock symbol to get the price for

		Returns:
		the stock price in euros
		"""
		return stocks_service.get_stock_price(stock)
