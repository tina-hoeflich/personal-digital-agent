from usecases.usecase import UseCase
from services.tankerkoenig import get_fuelprice
from services.stocks import get_stock_price

class SparenUseCase(UseCase):
	def get_triggerwords(self) -> list[str]:
		return ["save", "discount", "stock", "gas", "car", "fuel", "money", "cheap", "cheaply"]

	def trigger(sefl) -> str:
		# hier kommt das periodische checken für proaktive Dinge rein.

		# hier muss jeder trigger noch den nächsten run schedulen. Aktuell geht das nicht, wir haben ja noch keinen scheduler.

		# hier kommt der text der an den user gelesen wird hin
		return "Periodic trigger of the example usecase"

	def asked(sefl, input: str) -> str:
		if "fuel" in input:
			# lat und long sind der Porscheplatz 1 in Stuttgart
			location, price = get_fuelprice("e5", 48.83421132375812, 9.152560823835184, 5)
			return "The currently lowest E5 fuel price is {}€ at {:.3f}.".format(price, location)
		if "stock" in input:
			symbol = "P911.DEX"
			price = get_stock_price(symbol)
			return "The stock price of {} is {:.2f}€.".format(symbol, price)
