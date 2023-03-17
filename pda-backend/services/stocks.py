from alpha_vantage.timeseries import TimeSeries

APIKEY = "5MECCCPWG3K5D69X"

def get_stock_price(symbol: str) -> float:
	# get the current stock price for a given symbol with alpha_vantage using the GLOBAL_QUOTE api
	ts = TimeSeries(key=APIKEY, output_format='json')
	data, _ = ts.get_quote_endpoint(symbol=symbol)
	return float(data["05. price"])
