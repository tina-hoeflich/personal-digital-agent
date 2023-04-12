import os

import services.tankerkoenig as tankerkoenig


def test_get_fuelprice():
	os.environ["TANKERKOENIG_API_KEY"] = "5764c28e-6601-cf68-01ec-c81ccc04eec4"
	location, price = tankerkoenig.get_fuelprice("e10", 48.78486972213759, 9.181908387899563, 5)
	assert type(location) == str
	assert type(price) == float
	assert "Stuttgart".lower() in location.lower()
	assert price < 2.10
	assert price > 1.00
