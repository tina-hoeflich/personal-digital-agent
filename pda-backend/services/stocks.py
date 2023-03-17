import requests

ENDPOINT = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&apikey=5MECCCPWG3K5D69X&symbol="

def get_stock_price(symbol: str) -> float:
	response = requests.get(ENDPOINT + symbol)
	price = response.json()["Global Quote"]["05. price"]
	return float(price)
