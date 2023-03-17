import pytankerkoenig as tankerkoenig

APIKEY = "5764c28e-6601-cf68-01ec-c81ccc04eec4"

def get_fuelprice(type: str, lat: float, long: float, radius: int) -> tuple[str, float]:
	"""Get the currently lowest fuel price for a given fuel type at the current location in a defined radius.

	Args:
		type (str): fuel type. supports e10, e5, diesel

	Returns:
		float: the lowest fuel price in the defined radius
	"""
	stationsInRadius = tankerkoenig.getNearbyStations(APIKEY, str(lat), str(long), str(radius), type, "price")
	bestPrice = stationsInRadius["stations"][0]["price"]
	location = stationsInRadius["stations"][0]["name"] + ", " + stationsInRadius["stations"][0]["street"] + ", " + stationsInRadius["stations"][0]["place"]
	return location, bestPrice
