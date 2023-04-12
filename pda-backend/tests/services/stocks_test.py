import os

import services.stocks as stocks


def test_get_stocks():
	os.environ["ALPHAVANTAGE_API_KEY"] = "5MECCCPWG3K5D69X"
	price = stocks.get_stock_price("MSFT")
	assert type(price) == float
	assert price > 10
	assert price < 1000
