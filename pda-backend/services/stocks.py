import os

from alpha_vantage.timeseries import TimeSeries

APIKEY = os.environ.get("ALPHAVANTAGE_API_KEY")


def get_stock_price(symbol: str) -> float:
	"""Get the stock price of the given symbol

	Args:
		symbol (str): ticker symbol to get the stock price for

	Returns:
		float: the current stock price of the given symbol
	"""
	# get the current stock price for a given symbol with alpha_vantage using the GLOBAL_QUOTE api
	ts = TimeSeries(key=APIKEY, output_format='json')
	data, _ = ts.get_quote_endpoint(symbol=symbol)
	return float(data["05. price"])
