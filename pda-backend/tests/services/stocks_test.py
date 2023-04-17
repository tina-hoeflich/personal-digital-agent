import os

import services.stocks as stocks


def test_get_stocks():
	price = stocks.get_stock_price("MSFT")
	assert type(price) == float
	assert price > 10
	assert price < 1000
