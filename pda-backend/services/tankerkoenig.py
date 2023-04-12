import os

import pytankerkoenig as tankerkoenig

APIKEY = os.environ.get("TANKERKOENIG_API_KEY")


def get_fuelprice(fuel_type: str, lat: float, long: float, radius: int) -> tuple[str, float]:
	"""Get the lowest current fuel price for a given fuel type at the current location in a defined radius.

	Args:
		fuel_type (str): fuel type. supports e10, e5, diesel
		lat (float): latitude of the search location
		long (float): longitude of the search location
		radius (int): search radius for fuel stations

	Returns:
		str: the location of the fuel station with the lowest radius
		float: the lowest fuel price in the defined radius
	"""
	stationsInRadius = tankerkoenig.getNearbyStations(APIKEY, str(lat), str(long), str(radius), fuel_type, "price")
	bestPrice = stationsInRadius["stations"][0]["price"]
	location = stationsInRadius["stations"][0]["name"] + ", " + stationsInRadius["stations"][0]["street"] + ", " + stationsInRadius["stations"][0]["place"]
	return location, bestPrice
